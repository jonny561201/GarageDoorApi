from mock import patch

from svc.routes.thermostat_routes import get_temperature


@patch('svc.routes.thermostat_routes.get_user_temp')
def test_get_temperature__should_call_thermostat_controller(mock_controller):
    get_temperature()

    mock_controller.assert_called()
