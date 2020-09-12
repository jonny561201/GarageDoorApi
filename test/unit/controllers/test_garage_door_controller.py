import json
import os
from datetime import datetime
from threading import Event

import jwt
from mock import patch

from svc.constants.garage_state import GarageState
from svc.constants.home_automation import Automation
from svc.controllers.garage_door_controller import get_status, update_state, toggle_door
from svc.services.garage_door import monitor_status
from svc.utilities.event_utils import MyThread


@patch('svc.controllers.garage_door_controller.is_jwt_valid')
@patch('svc.controllers.garage_door_controller.gpio_utils')
@patch('svc.controllers.garage_door_controller.create_thread')
class TestGarageController:
    GARAGE_ID = '2'
    STATE = GarageState.get_instance().DOORS[GARAGE_ID]
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')
    REQUEST = '{"openGarage": "True"}'.encode()

    def setup_method(self):
        self.STATE.ACTIVE_THREAD = None
        self.STATE.STOP_EVENT = None
        self.STATE.CLOSED_TIME = None
        self.STATE.OPEN_TIME = None
        self.STATE.STATUS = None
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    def test_get_status__should_call_is_garage_door_open_status(self, mock_thread, mock_gpio, mock_jwt):
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        mock_gpio.is_garage_open.assert_called_with(self.GARAGE_ID)

    @patch('svc.controllers.garage_door_controller.datetime')
    def test_get_status__should_return_status(self, mock_date, mock_thread, mock_gpio, mock_jwt):
        now = datetime.now()
        mock_date.now.return_value = now
        mock_gpio.is_garage_open.return_value = True
        coords = {'lat': 12.2, 'lon': 84.3}
        mock_gpio.get_garage_coordinates.return_value = coords
        expected_body = {"isGarageOpen": True, 'statusDuration': now, 'coordinates': coords}

        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual == expected_body

    def test_get_status__should_create_thread_when_no_active_thread(self, mock_thread, mock_gpio, mock_jwt):
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        mock_thread.assert_called_with(self.STATE, monitor_status, self.GARAGE_ID)

    def test_get_status__should_create_thread_when_active_thread_with_different_garage_id(self, mock_thread, mock_gpio, mock_jwt):
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        mock_thread.assert_called_with(self.STATE, monitor_status, self.GARAGE_ID)

    def test_get_status__should_set_state_of_thread_after_initial_check(self, mock_thread, mock_gpio, mock_jwt):
        mock_gpio.is_garage_open.return_value = True
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert self.STATE.STATUS is True

    def test_get_status__should_return_garage_state_status_when_active_thread(self, mock_thread, mock_gpio, mock_jwt):
        self.STATE.ACTIVE_THREAD = MyThread(Event(), print, self.GARAGE_ID, Automation.TIMING.THIRTY_SECONDS)
        self.STATE.STATUS = False

        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual['isGarageOpen'] is False

    def test_get_status__should_return_open_garage_status_date_when_active_thread(self, mock_thread, mock_gpio, mock_jwt):
        self.STATE.ACTIVE_THREAD = MyThread(Event(), print, self.GARAGE_ID, Automation.TIMING.THIRTY_SECONDS)
        now = datetime.now()
        self.STATE.STATUS = False
        self.STATE.CLOSED_TIME = now

        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual['statusDuration'] == now

    def test_get_status__should_return_close_garage_status_date_when_active_thread(self, mock_thread, mock_gpio, mock_jwt):
        self.STATE.ACTIVE_THREAD = MyThread(Event(), print, self.GARAGE_ID, Automation.TIMING.THIRTY_SECONDS)
        now = datetime.now()
        self.STATE.STATUS = True
        self.STATE.OPEN_TIME = now

        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual['statusDuration'] == now

    def test_get_status__should_call_is_jwt_valid(self, mock_thread, mock_gpio, mock_jwt):
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        mock_jwt.assert_called_with(self.JWT_TOKEN)

    def test_get_status__should_call_gpio_util_to_get_coordinates(self, mock_thread,mock_gpio, mock_jwt):
        get_status(self.JWT_TOKEN, self.GARAGE_ID)

        mock_gpio.get_garage_coordinates.assert_called()

    def test_get_status__should_return_gpio_coords_in_get_status_response(self, mock_thread, mock_gpio, mock_jwt):
        coords = {'latitude': 12.2, 'longitude': -94.23}
        self.STATE.ACTIVE_THREAD = MyThread(Event(), print, self.GARAGE_ID, Automation.TIMING.THIRTY_SECONDS)
        mock_gpio.get_garage_coordinates.return_value = coords
        actual = get_status(self.JWT_TOKEN, self.GARAGE_ID)

        assert actual['coordinates'] == coords

    def test_update_state__should_validate_jwt(self, mock_thread, mock_gpio, mock_jwt):
        mock_gpio.update_garage_door.return_value = False

        update_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        mock_jwt.assert_called()

    def test_update_state__should_return_response(self, mock_thread, mock_gpio, mock_jwt):
        mock_gpio.update_garage_door.return_value = False

        actual = update_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        assert actual == {'garageDoorOpen': False}

    def test_update_state__should_call_update_gpio(self, mock_thread, mock_gpio, mock_jwt):
        expected_request = json.loads(self.REQUEST.decode('UTF-8'))
        update_state(self.JWT_TOKEN, self.GARAGE_ID, self.REQUEST)

        mock_gpio.update_garage_door.assert_called_with(self.GARAGE_ID, expected_request)

    def test_toggle_garage_door_state__should_validate_bearer_token(self, mock_thread, mock_gpio, mock_jwt):
        toggle_door(self.JWT_TOKEN, self.GARAGE_ID)

        mock_jwt.assert_called_with(self.JWT_TOKEN)

    def test_toggle_garage_door_state__should_call_gpio_pins(self, mock_thread, mock_gpio, mock_jwt):
        toggle_door(self.JWT_TOKEN, self.GARAGE_ID)

        mock_gpio.toggle_garage_door.assert_called_with(self.GARAGE_ID)
