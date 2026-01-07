from mock import patch

from svc.config.settings_state import Settings
from svc.utilities.gpio_utils import update_garage_door, get_garage_coordinates

GARAGE_ID = 2


@patch('svc.utilities.gpio_utils.toggle_garage_door')
@patch('svc.utilities.gpio_utils.is_garage_open')
def test_update_garage_door__should_toggle_garage_when_open_and_request_close(mock_status, mock_toggle):
    request = {'garageDoorOpen': False}
    mock_status.return_value = True
    update_garage_door(GARAGE_ID, request)

    mock_toggle.assert_called()


@patch('svc.utilities.gpio_utils.toggle_garage_door')
@patch('svc.utilities.gpio_utils.is_garage_open')
def test_update_garage_door__should_toggle_garage_when_close_and_request_open(mock_status, mock_toggle):
    request = {'garageDoorOpen': True}
    mock_status.return_value = False
    update_garage_door(GARAGE_ID, request)

    mock_toggle.assert_called()


@patch('svc.utilities.gpio_utils.toggle_garage_door')
@patch('svc.utilities.gpio_utils.is_garage_open')
def test_update_garage_door__should_not_toggle_garage_when_close_and_request_close(mock_status, mock_toggle):
    request = {'garageDoorOpen': False}
    mock_status.return_value = False
    update_garage_door(GARAGE_ID, request)

    mock_toggle.assert_not_called()


@patch('svc.utilities.gpio_utils.toggle_garage_door')
@patch('svc.utilities.gpio_utils.is_garage_open')
def test_update_garage_door__should_not_toggle_garage_when_open_and_request_open(mock_status, mock_toggle):
    request = {'garageDoorOpen': True}
    mock_status.return_value = True
    update_garage_door(GARAGE_ID, request)

    mock_toggle.assert_not_called()


@patch('svc.utilities.gpio_utils.toggle_garage_door')
@patch('svc.utilities.gpio_utils.is_garage_open')
def test_update_garage_door__should_return_false_when_closing(mock_status, mock_toggle):
    request = {'garageDoorOpen': False}
    mock_status.return_value = True
    actual = update_garage_door(GARAGE_ID, request)

    assert actual is False


@patch('svc.utilities.gpio_utils.toggle_garage_door')
@patch('svc.utilities.gpio_utils.is_garage_open')
def test_update_garage_door__should_return_true_when_opening(mock_status, mock_toggle):
    request = {'garageDoorOpen': True}
    mock_status.return_value = False
    actual = update_garage_door(GARAGE_ID, request)

    assert actual is True


def test_get_garage_coordinates__should_return_settings_coords():
    instance = Settings.get_instance()
    instance.Coordinates._settings = {'latitude': 10.0, 'longitude': 20.0}

    actual = get_garage_coordinates()

    assert actual.latitude == 10.0
    assert actual.longitude == 20.0