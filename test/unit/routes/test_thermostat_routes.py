import jwt
from mock import patch, ANY

from svc.routes.thermostat_routes import get_temperature, set_temperature


@patch('svc.routes.thermostat_routes.SetThermostat')
@patch('svc.routes.thermostat_routes.request')
@patch('svc.routes.thermostat_routes.get_user_temp')
class TestThermostatRoutes:
    JWT_TOKEN = jwt.encode({}, 'JWT_SECRET', algorithm='HS256').decode('UTF-8')
    BEARER_TOKEN = "Bearer " + JWT_TOKEN
    AUTH_HEADER = {"Authorization": BEARER_TOKEN}
    USER_ID = 'test'

    def test_get_temperature__should_call_thermostat_controller(self, mock_controller, mock_request, mock_set):
        get_temperature(self.USER_ID)

        mock_controller.assert_called()

    def test_get_temperature__should_call_thermostat_controller_with_correct_parameters(self, mock_controller, mock_request, mock_set):
        mock_request.headers = self.AUTH_HEADER
        get_temperature(self.USER_ID)

        mock_controller.assert_called_with(self.USER_ID, self.BEARER_TOKEN)

    def test_get_temperature__should_return_response_from_controller(self, mock_controller, mock_request, mock_set):
        expected_temp = {'currentTemp': 34.12}
        mock_controller.return_value = expected_temp

        actual = get_temperature(self.USER_ID)

        assert actual == expected_temp

    def test_set_temperature__should_call_thermostat_controller(self, mock_controller, mock_request, mock_set):
        set_temperature(self.USER_ID)

        mock_set.assert_called()

    def test_set_temperature__should_call_thermostat_controller_with_bearer_token(self, mock_controller, mock_request, mock_set):
        mock_request.headers = self.AUTH_HEADER
        set_temperature(self.USER_ID)

        mock_set.return_value.set_user_temperature.assert_called_with(ANY, self.BEARER_TOKEN)

    def test_set_temperature__should_call_thermostat_controller_with_request_body(self, mock_controller, mock_request, mock_set):
        request = {'desiredTemp': 34.1}
        mock_request.data = request

        set_temperature(self.USER_ID)

        mock_set.return_value.set_user_temperature.assert_called_with(request, ANY)
