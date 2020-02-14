from mock import patch

from svc.routes.light_routes import get_all_assigned_lights


@patch('svc.routes.light_routes.request')
@patch('svc.routes.light_routes.get_assigned_lights')
class TestLightRoutes:

    def test_get_all_assigned_lights__should_call_get_assigned_lights(self, mock_controller, mock_request):
        bearer_token = 'not real'
        mock_request.headers = {'Authorization': bearer_token}

        get_all_assigned_lights()

        mock_controller.assert_called_with(bearer_token)

    def test_get_all_assigned_lights__should_return_success_status_code(self, mock_controller, mock_request):
        actual = get_all_assigned_lights()

        assert actual.status_code == 200

    def test_get_all_assigned_lights__should_return_success_headers(self, mock_controller, mock_request):
        actual = get_all_assigned_lights()

        assert actual.content_type == 'text/json'

