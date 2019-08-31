import uuid

from mock import patch

from svc.controllers.thermostat_controller import get_user_temp


@patch('svc.controllers.thermostat_controller.read_temperature_file')
def test_get_user_temp__should_call_read_temperature_file(mock_temp_file):
    user_id = uuid.uuid4().hex

    get_user_temp(user_id)

    mock_temp_file.assert_called()
