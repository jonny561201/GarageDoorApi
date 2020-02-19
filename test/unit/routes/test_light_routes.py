import json

from mock import patch

from svc.routes.light_routes import get_all_assigned_lights, set_assigned_light_group


@patch('svc.routes.light_routes.request')
@patch('svc.routes.light_routes.light_controller')
class TestLightRoutes:

    def test_get_all_assigned_lights__should_call_get_assigned_lights(self, mock_controller, mock_request):
        bearer_token = 'not real'
        mock_request.headers = {'Authorization': bearer_token}
        mock_controller.get_assigned_lights.return_value = {}

        get_all_assigned_lights()

        mock_controller.get_assigned_lights.assert_called_with(bearer_token)

    def test_get_all_assigned_lights__should_return_success_status_code(self, mock_controller, mock_request):
        mock_controller.get_assigned_lights.return_value = {}
        actual = get_all_assigned_lights()

        assert actual.status_code == 200

    def test_get_all_assigned_lights__should_return_success_headers(self, mock_controller, mock_request):
        mock_controller.get_assigned_lights.return_value = {}
        actual = get_all_assigned_lights()

        assert actual.content_type == 'text/json'

    def test_get_all_assigned_lights__should_response_from_controller(self, mock_controller, mock_request):
        result = {'response': 'not important'}
        mock_controller.get_assigned_lights.return_value = result
        actual = get_all_assigned_lights()

        assert json.loads(actual.data) == result

    def test_set_assigned_light_group__should_call_light_controller(self, mock_controller, mock_request):
        bearer_token = 'fakeBearer'
        request_data = '{"on": "False", "groupId": 1}'
        mock_request.headers = {'Authorization': bearer_token}
        mock_request.data = request_data.encode()

        set_assigned_light_group()

        mock_controller.set_assigned_lights.assert_called_with(bearer_token, json.loads(request_data))

    def test_set_assigned_light_group__should_return_success_status_code(self, mock_controller, mock_request):
        mock_request.data = '{}'.encode('UTF-8')
        actual = set_assigned_light_group()

        assert actual.status_code == 200

    def test_set_assigned_light_group__should_return_success_headers(self, mock_controller, mock_request):
        mock_request.data = '{}'.encode('UTF-8')
        actual = set_assigned_light_group()

        assert actual.content_type == 'text/json'
