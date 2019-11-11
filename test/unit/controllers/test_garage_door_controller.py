import json
import os

import jwt
from mock import patch

from svc.controllers.garage_door_controller import get_status, update_state, toggle_garage_door_state


class TestGarageController:
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')
    REQUEST = '{"openGarage": "True"}'.encode()

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    @patch('svc.controllers.garage_door_controller.garage_door_status')
    def test_garage_door_status__should_call_get_garage_door_status(self, mock_gpio):
        mock_gpio.return_value = {}
        get_status(self.JWT_TOKEN)

        mock_gpio.assert_called()

    def test_garage_door_status__should_return_status(self):
        expected_body = {"isGarageOpen": True}

        actual = get_status(self.JWT_TOKEN)

        assert actual == expected_body

    @patch('svc.controllers.garage_door_controller.is_jwt_valid')
    def test_garage_door_status__should_call_is_jwt_valid(self, mock_validate):
        get_status(self.JWT_TOKEN)

        mock_validate.assert_called_with(self.JWT_TOKEN)

    @patch('svc.controllers.garage_door_controller.update_garage_door')
    def test_update_garage_door_state__should_return_response_(self, mock_gpio):
        mock_gpio.return_value = False

        actual = update_state(self.JWT_TOKEN, self.REQUEST)

        assert actual == {'garageDoorOpen': False}

    @patch('svc.controllers.garage_door_controller.update_garage_door')
    def test_update_garage_door_state__should_call_update_gpio(self, mock_gpio):
        expected_request = json.loads(self.REQUEST.decode('UTF-8'))
        update_state(self.JWT_TOKEN, self.REQUEST)

        mock_gpio.assert_called_with(expected_request)

    @patch('svc.controllers.garage_door_controller.is_jwt_valid')
    def test_toggle_garage_door_state__should_validate_bearer_token(self, mock_jwt):
        toggle_garage_door_state(self.JWT_TOKEN)

        mock_jwt.assert_called_with(self.JWT_TOKEN)

    @patch('svc.controllers.garage_door_controller.toggle_garage_door')
    def test_toggle_garage_door_state__should_call_gpio_pins(self, mock_toggle):
        toggle_garage_door_state(self.JWT_TOKEN)

        mock_toggle.assert_called()
