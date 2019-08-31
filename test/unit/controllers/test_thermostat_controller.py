import uuid

from mock import patch

from svc.controllers.thermostat_controller import get_user_temp


@patch('svc.controllers.thermostat_controller.get_user_temperature')
@patch('svc.controllers.thermostat_controller.read_temperature_file')
def test_get_user_temp__should_call_read_temperature_file(mock_temp_file, mock_user_temp):
    user_id = uuid.uuid4().hex

    get_user_temp(user_id)

    mock_temp_file.assert_called()


@patch('svc.controllers.thermostat_controller.read_temperature_file')
@patch('svc.controllers.thermostat_controller.get_user_temperature')
def test_get_user_temp__should_call_get_user_temperature(mock_user_temp, mock_temp_file):
    user_id = uuid.uuid4().hex
    temp_text = 'fake response'
    mock_temp_file.return_value = temp_text

    get_user_temp(user_id)

    mock_user_temp.assert_called_with(temp_text, False)
