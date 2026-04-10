from datetime import datetime

import pytest
from mock import patch
from werkzeug.exceptions import BadRequest

from svc.config.settings_state import Coordinates
from svc.controllers.garage_door_controller import get_status, update_door_state, toggle_door, get_all_statuses


@patch('svc.controllers.garage_door_controller.file_utils')
@patch('svc.controllers.garage_door_controller.validate_api_key')
@patch('svc.controllers.garage_door_controller.gpio_utils')
class TestGarageController:
    GARAGE_ID = '2'
    API_KEY = 'fake_api_key'
    REQUEST = '{"open": true}'.encode()

    def test_get_status__should_return_garage_status_when_active_thread(self, mock_gpio, mock_validate, mock_file):
        mock_gpio.is_garage_open.return_value = False

        actual = get_status(self.API_KEY, self.GARAGE_ID)

        assert actual.isGarageOpen is False

    def test_get_status__should_return_open_garage_status_date(self, mock_gpio, mock_validate, mock_file):
        now = datetime.now()
        mock_file.get_door_duration.return_value = now

        actual = get_status(self.API_KEY, self.GARAGE_ID)

        assert actual.statusDuration == now

    def test_get_status__should_validate_api_key(self, mock_gpio, mock_validate, mock_file):
        get_status(self.API_KEY, self.GARAGE_ID)

        mock_validate.assert_called_with(self.API_KEY)

    def test_get_status__should_call_gpio_util_to_get_coordinates(self, mock_gpio, mock_validate, mock_file):
        get_status(self.API_KEY, self.GARAGE_ID)

        mock_gpio.get_garage_coordinates.assert_called()

    def test_get_status__should_return_gpio_coordinates(self, mock_gpio, mock_validate, mock_file):
        coords = Coordinates({'latitude': 12.2, 'longitude': -94.23})
        mock_gpio.get_garage_coordinates.return_value = coords
        actual = get_status(self.API_KEY, self.GARAGE_ID)

        assert actual.coordinates.latitude == coords.latitude
        assert actual.coordinates.longitude == coords.longitude

    def test_update_door_state__should_validate_api_key(self, mock_gpio, mock_validate, mock_file):
        mock_gpio.update_garage_door.return_value = False

        update_door_state(self.API_KEY, self.GARAGE_ID, self.REQUEST)

        mock_validate.assert_called_with(self.API_KEY)

    def test_update_door_state__should_return_response(self, mock_gpio, mock_validate, mock_file):
        mock_gpio.is_garage_open.return_value = True

        actual = update_door_state(self.API_KEY, self.GARAGE_ID, self.REQUEST)

        assert actual.isGarageOpen == True

    def test_update_door_state__should_call_toggle_when_state_is_different_than_request(self, mock_gpio, mock_validate, mock_file):
        mock_gpio.is_garage_open.return_value = False
        actual = update_door_state(self.API_KEY, self.GARAGE_ID, self.REQUEST)

        mock_gpio.toggle_garage_door.assert_called_with(self.GARAGE_ID)
        assert actual.isGarageOpen == True

    def test_update_door_state__should_not_toggle_when_state_is_same_as_request(self, mock_gpio, mock_validate, mock_file):
        mock_gpio.is_garage_open.return_value = True
        actual = update_door_state(self.API_KEY, self.GARAGE_ID, self.REQUEST)

        mock_gpio.toggle_garage_door.assert_not_called()
        assert actual.isGarageOpen == True

    def test_update_door_state__should_raise_bad_request_when_key_not_found(self, mock_gpio, mock_validate, mock_file):
        bad_request = '{"fake": true}'.encode()
        with pytest.raises(BadRequest):
            update_door_state(self.API_KEY, self.GARAGE_ID, bad_request)

    def test_toggle_garage__should_validate_api_key(self, mock_gpio, mock_validate, mock_file):
        toggle_door(self.API_KEY, self.GARAGE_ID)

        mock_validate.assert_called_with(self.API_KEY)

    def test_toggle_garage__should_call_gpio_pins(self, mock_gpio, mock_validate, mock_file):
        toggle_door(self.API_KEY, self.GARAGE_ID)

        mock_gpio.toggle_garage_door.assert_called_with(self.GARAGE_ID)

    def test_toggle_garage_door__should_call_update_door_duration(self, mock_gpio, mock_validate, mock_file):
        toggle_door(self.API_KEY, self.GARAGE_ID)

        mock_file.update_door_duration.assert_called_with(self.GARAGE_ID)

    def test_get_all_statuses__should_validate_api_key(self, mock_gpio, mock_validate, mock_file):
        mock_file.get_door_duration.return_value = datetime.now()
        get_all_statuses(self.API_KEY)

        mock_validate.assert_called_once_with(self.API_KEY)

    def test_get_all_statuses__should_return_two_doors(self, mock_gpio, mock_validate, mock_file):
        mock_file.get_door_duration.return_value = datetime.now()
        mock_gpio.is_garage_open.return_value = False

        actual = get_all_statuses(self.API_KEY)

        assert len(actual.doors) == 2
        assert actual.doors[0].garageId == '1'
        assert actual.doors[1].garageId == '2'

    def test_get_all_statuses__should_call_coordinates_once(self, mock_gpio, mock_validate, mock_file):
        mock_file.get_door_duration.return_value = datetime.now()

        get_all_statuses(self.API_KEY)

        mock_gpio.get_garage_coordinates.assert_called_once()

    def test_get_all_statuses__should_return_coordinates_on_top_level(self, mock_gpio, mock_validate, mock_file):
        mock_file.get_door_duration.return_value = datetime.now()
        coords = Coordinates({'latitude': 12.2, 'longitude': -94.23})
        mock_gpio.get_garage_coordinates.return_value = coords

        actual = get_all_statuses(self.API_KEY)

        assert actual.coordinates.latitude == coords.latitude
        assert actual.coordinates.longitude == coords.longitude

    def test_get_all_statuses__should_return_open_status_per_door(self, mock_gpio, mock_validate, mock_file):
        mock_file.get_door_duration.return_value = datetime.now()
        mock_gpio.is_garage_open.side_effect = [True, False]

        actual = get_all_statuses(self.API_KEY)

        assert actual.doors[0].isGarageOpen is True
        assert actual.doors[1].isGarageOpen is False

