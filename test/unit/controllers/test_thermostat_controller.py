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


@patch('svc.controllers.thermostat_controller.read_temperature_file')
@patch('svc.controllers.thermostat_controller.get_user_temperature')
def test_get_user_temp__should_return_response_from_get_user_temperature(mock_user_temp, mock_temp_file):
    user_id = uuid.uuid4().hex
    expected_temp = 23.45
    mock_user_temp.return_value = expected_temp

    actual = get_user_temp(user_id)

    assert actual == expected_temp
