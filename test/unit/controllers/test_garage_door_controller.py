import os
from datetime import datetime

import jwt
import pytest
from mock import patch
from werkzeug.exceptions import BadRequest

from svc.config.settings_state import Coordinates
from svc.controllers.garage_door_controller import get_status, update_door_state, toggle_door


@patch('svc.controllers.garage_door_controller.file_utils')
@patch('svc.controllers.garage_door_controller.is_jwt_valid')
@patch('svc.controllers.garage_door_controller.gpio_utils')
class TestGarageController:
    GARAGE_ID = '2'
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256')
    REQUEST = '{"open": true}'.encode()

    def setup_method(self):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    def test_get_status__should_return_garage_status_when_active_thread(self, mock_gpio, mock_jwt, mock_file):
        mock_gpio.is_garage_open.return_value = False

        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual.isGarageOpen is False

    def test_get_status__should_return_open_garage_status_date(self, mock_gpio, mock_jwt, mock_file):
        now = datetime.now()
        mock_file.get_door_duration.return_value = now

        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual.statusDuration == now

    def test_get_status__should_call_is_jwt_valid(self, mock_gpio, mock_jwt, mock_file):
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        mock_jwt.assert_called_with(self.JWT_TOKEN)

    def test_get_status__should_call_gpio_util_to_get_coordinates(self,mock_gpio, mock_jwt, mock_file):
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        mock_gpio.get_garage_coordinates.assert_called()

    def test_get_status__should_return_gpio_coordinates(self, mock_gpio, mock_jwt, mock_file):
        coords = Coordinates({'latitude': 12.2, 'longitude': -94.23})
        mock_gpio.get_garage_coordinates.return_value = coords
        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual.coordinates.latitude == coords.latitude
        assert actual.coordinates.longitude == coords.longitude

    def test_update_door_state__should_validate_jwt(self, mock_gpio, mock_jwt, mock_file):
        mock_gpio.update_garage_door.return_value = False

        update_door_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        mock_jwt.assert_called()

    def test_update_door_state__should_return_response(self, mock_gpio, mock_jwt, mock_file):
        mock_gpio.is_garage_open.return_value = True

        actual = update_door_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        assert actual.isGarageOpen ==  True

    def test_update_door_state__should_call_toggle_when_state_is_different_than_request(self, mock_gpio, mock_jwt, mock_file):
        mock_gpio.is_garage_open.return_value = False
        actual = update_door_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        mock_gpio.toggle_garage_door.assert_called_with(self.GARAGE_ID)
        assert actual.isGarageOpen == True

    def test_update_door_state__should_not_toggle_when_state_is_same_as_request(self, mock_gpio, mock_jwt, mock_file):
        mock_gpio.is_garage_open.return_value = True
        actual = update_door_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        mock_gpio.toggle_garage_door.assert_not_called()
        assert actual.isGarageOpen == True

    def test_update_door_state__should_raise_bad_request_when_key_not_found(self, mock_gpio, mock_jwt, mock_file):
        bad_request = '{"fake": true}'.encode()
        with pytest.raises(BadRequest):
            update_door_state(self.JWT_TOKEN, self.GARAGE_ID, bad_request)

    def test_toggle_garage__should_validate_bearer_token(self, mock_gpio, mock_jwt, mock_file):
        toggle_door(self.JWT_TOKEN, self.GARAGE_ID)

        mock_jwt.assert_called_with(self.JWT_TOKEN)

    def test_toggle_garage__should_call_gpio_pins(self, mock_gpio, mock_jwt, mock_file):
        toggle_door(self.JWT_TOKEN, self.GARAGE_ID)

        mock_gpio.toggle_garage_door.assert_called_with(self.GARAGE_ID)

    def test_toggle_garage_door__should_call_update_door_duration(self, mock_gpio, mock_jwt, mock_file):
        toggle_door(self.JWT_TOKEN, self.GARAGE_ID)

        mock_file.update_door_duration.assert_called_with(self.GARAGE_ID)
