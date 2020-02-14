from mock import patch

from svc.routes.light_routes import get_all_assigned_lights


@patch('svc.routes.light_routes.request')
@patch('svc.routes.light_routes.get_assigned_lights')
def test_get_all_assigned_lights__should_call_get_assigned_lights(mock_controller, mock_request):
    bearer_token = 'not real'
    mock_request.headers = {'Authorization': bearer_token}

    get_all_assigned_lights()

    mock_controller.assert_called_with(bearer_token)
