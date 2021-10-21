import json
import os
from datetime import datetime

import jwt
from mock import patch

from svc.controllers.garage_door_controller import get_status, update_state, toggle_door


@patch('svc.controllers.garage_door_controller.get_door_duration')
@patch('svc.controllers.garage_door_controller.is_jwt_valid')
@patch('svc.controllers.garage_door_controller.gpio_utils')
class TestGarageController:
    GARAGE_ID = '2'
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')
    REQUEST = '{"openGarage": "True"}'.encode()

    def setup_method(self):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    def test_get_status__should_return_garage_status_when_active_thread(self, mock_gpio, mock_jwt, mock_duration):
        mock_gpio.is_garage_open.return_value = False

        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual['isGarageOpen'] is False

    def test_get_status__should_return_open_garage_status_date(self, mock_gpio, mock_jwt, mock_duration):
        now = datetime.now()
        mock_duration.return_value = now

        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual['statusDuration'] == now

    def test_get_status__should_call_is_jwt_valid(self, mock_gpio, mock_jwt, mock_duration):
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        mock_jwt.assert_called_with(self.JWT_TOKEN)

    def test_get_status__should_call_gpio_util_to_get_coordinates(self,mock_gpio, mock_jwt, mock_duration):
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        mock_gpio.get_garage_coordinates.assert_called()

    def test_get_status__should_return_gpio_coordinates(self, mock_gpio, mock_jwt, mock_duration):
        coords = {'latitude': 12.2, 'longitude': -94.23}
        mock_gpio.get_garage_coordinates.return_value = coords
        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual['coordinates'] == coords

    def test_update_state__should_validate_jwt(self, mock_gpio, mock_jwt, mock_duration):
        mock_gpio.update_garage_door.return_value = False

        update_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        mock_jwt.assert_called()

    def test_update_state__should_return_response(self, mock_gpio, mock_jwt, mock_duration):
        mock_gpio.update_garage_door.return_value = False

        actual = update_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        assert actual == {'isGarageOpen': False}

    def test_update_state__should_call_update_gpio(self, mock_gpio, mock_jwt, mock_duration):
        expected_request = json.loads(self.REQUEST.decode('UTF-8'))
        update_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        mock_gpio.update_garage_door.assert_called_with(self.GARAGE_ID, expected_request)

    def test_toggle_garage_door_state__should_validate_bearer_token(self, mock_gpio, mock_jwt, mock_duration):
        toggle_door(self.JWT_TOKEN, self.GARAGE_ID)

        mock_jwt.assert_called_with(self.JWT_TOKEN)

    def test_toggle_garage_door_state__should_call_gpio_pins(self, mock_gpio, mock_jwt, mock_duration):
        toggle_door(self.JWT_TOKEN, self.GARAGE_ID)

        mock_gpio.toggle_garage_door.assert_called_with(self.GARAGE_ID)
