from mock import patch

from svc.routes.sump_routes import get_current_sump_level


@patch('svc.routes.sump_routes.get_sump_level')
def test_get_current_sump_level__should_call_controller(mock_controller):
    user_id = 'fakeuserid'
    get_current_sump_level(user_id)

    mock_controller.assert_called_with(user_id)
