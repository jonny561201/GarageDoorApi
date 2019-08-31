import jwt
from mock import patch

from svc.routes.thermostat_routes import get_temperature


@patch('svc.routes.thermostat_routes.request')
@patch('svc.routes.thermostat_routes.get_user_temp')
class TestThermostatRoutes:
    JWT_TOKEN = jwt.encode({}, 'JWT_SECRET', algorithm='HS256').decode('UTF-8')
    BEARER_TOKEN = "Bearer " + JWT_TOKEN
    AUTH_HEADER = {"Authorization": BEARER_TOKEN}

    def test_get_temperature__should_call_thermostat_controller(self, mock_controller, mock_request):
        get_temperature()

        mock_controller.assert_called()

    def test_get_temperature__should_call_thermostat_controller_with_correct_parameters(self, mock_controller, mock_request):
        mock_request.headers = self.AUTH_HEADER
        get_temperature()

        mock_controller.assert_called_with(None, self.BEARER_TOKEN)

    def test_get_temperature__should_return_response_from_controller(self, mock_controller, mock_request):
        expected_temp = {'currentTemp': 34.12}
        mock_controller.return_value = expected_temp

        actual = get_temperature()

        assert actual == expected_temp
