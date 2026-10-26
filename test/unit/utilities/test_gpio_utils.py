from mock import patch

from svc.config.settings_state import Settings
from svc.utilities.gpio_utils import get_garage_coordinates, set_garage_door


def test_get_garage_coordinates__should_return_settings_coords():
    instance = Settings.get_instance()
    instance.Coordinates._settings = {'latitude': 10.0, 'longitude': 20.0}

    actual = get_garage_coordinates()

    assert actual.latitude == 10.0
    assert actual.longitude == 20.0


@patch('svc.utilities.gpio_utils.toggle_garage_door')
@patch('svc.utilities.gpio_utils.is_garage_open')
class TestSetGarageDoor:
    GARAGE_ID = '1'

    def test_set_garage_door__should_toggle_when_state_is_different_than_requested(self, mock_open, mock_toggle):
        mock_open.return_value = False

        actual = set_garage_door(self.GARAGE_ID, True)

        mock_toggle.assert_called_once_with(self.GARAGE_ID)
        assert actual is True

    def test_set_garage_door__should_not_toggle_when_state_is_same_as_requested(self, mock_open, mock_toggle):
        mock_open.return_value = True

        actual = set_garage_door(self.GARAGE_ID, True)

        mock_toggle.assert_not_called()
        assert actual is True
