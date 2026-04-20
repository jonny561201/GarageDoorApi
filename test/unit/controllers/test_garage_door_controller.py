import json
from datetime import datetime

import pytest
from mock import MagicMock, patch
from werkzeug.exceptions import BadRequest

from svc.config.settings_state import Coordinates
from svc.controllers.garage_door_controller import get_status, update_door_state, toggle_door, get_all_statuses, \
    update_door_worker, cancel_schedule


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

        assert actual.duration == now

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


@patch('svc.controllers.garage_door_controller.schedule_utils')
@patch('svc.controllers.garage_door_controller.file_utils')
@patch('svc.controllers.garage_door_controller.gpio_utils')
class TestUpdateDoorWorker:
    GARAGE_ID = '1'

    def _delivery(self):
        method = MagicMock()
        method.delivery_tag = 'tag'
        channel = MagicMock()
        return channel, method

    def _body(self, payload):
        return json.dumps(payload).encode('UTF-8')

    def test_schedule__should_delegate_to_schedule_utils(self, mock_gpio, mock_file, mock_schedule):
        channel, method = self._delivery()
        payload = {'id': self.GARAGE_ID, 'action': 'schedule', 'delay_seconds': 300}
        body = self._body(payload)

        update_door_worker(channel, method, None, body)

        mock_schedule.schedule_close.assert_called_once_with(self.GARAGE_ID, payload)
        channel.basic_ack.assert_called_once_with(delivery_tag='tag')

    def test_schedule__should_nack_when_schedule_close_raises(self, mock_gpio, mock_file, mock_schedule):
        channel, method = self._delivery()
        mock_schedule.schedule_close.side_effect = BadRequest
        body = self._body({'id': self.GARAGE_ID, 'action': 'schedule'})

        update_door_worker(channel, method, None, body)

        channel.basic_nack.assert_called_once_with(delivery_tag='tag', requeue=False)


@patch('svc.controllers.garage_door_controller.schedule_utils')
@patch('svc.controllers.garage_door_controller.validate_api_key')
class TestCancelSchedule:
    GARAGE_ID = '1'
    API_KEY = 'fake_api_key'

    def test_cancel_schedule__should_validate_api_key(self, mock_validate, mock_schedule):
        mock_schedule.cancel.return_value = False

        cancel_schedule(self.API_KEY, self.GARAGE_ID)

        mock_validate.assert_called_once_with(self.API_KEY)

    def test_cancel_schedule__should_return_cancelled_true_when_schedule_existed(self, mock_validate, mock_schedule):
        mock_schedule.cancel.return_value = True

        actual = cancel_schedule(self.API_KEY, self.GARAGE_ID)

        assert actual == {'cancelled': True}

    def test_cancel_schedule__should_return_cancelled_false_when_no_schedule(self, mock_validate, mock_schedule):
        mock_schedule.cancel.return_value = False

        actual = cancel_schedule(self.API_KEY, self.GARAGE_ID)

        assert actual == {'cancelled': False}
