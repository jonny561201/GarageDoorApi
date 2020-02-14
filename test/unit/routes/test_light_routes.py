import json

from mock import patch

from svc.routes.light_routes import get_all_assigned_lights


@patch('svc.routes.light_routes.request')
@patch('svc.routes.light_routes.get_assigned_lights')
class TestLightRoutes:

    def test_get_all_assigned_lights__should_call_get_assigned_lights(self, mock_controller, mock_request):
        bearer_token = 'not real'
        mock_request.headers = {'Authorization': bearer_token}
        mock_controller.return_value = {}

        get_all_assigned_lights()

        mock_controller.assert_called_with(bearer_token)

    def test_get_all_assigned_lights__should_return_success_status_code(self, mock_controller, mock_request):
        mock_controller.return_value = {}
        actual = get_all_assigned_lights()

        assert actual.status_code == 200

    def test_get_all_assigned_lights__should_return_success_headers(self, mock_controller, mock_request):
        mock_controller.return_value = {}
        actual = get_all_assigned_lights()

        assert actual.content_type == 'text/json'

    def test_get_all_assigned_lights__should_response_from_controller(self, mock_controller, mock_request):
        result = {'response': 'not important'}
        mock_controller.return_value = result
        actual = get_all_assigned_lights()

        assert json.loads(actual.data) == result

