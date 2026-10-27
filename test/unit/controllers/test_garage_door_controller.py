import json
from datetime import datetime

import pytest
from mock import MagicMock, patch
from werkzeug.exceptions import BadRequest, Unauthorized

from svc.config.settings_state import Coordinates
from svc.controllers.garage_door_controller import get_status, update_door_state, toggle_door, get_all_statuses, \
    cancel_schedule, stream_statuses


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
        update_door_state(self.API_KEY, self.GARAGE_ID, self.REQUEST)

        mock_validate.assert_called_with(self.API_KEY)

    def test_update_door_state__should_return_response(self, mock_gpio, mock_validate, mock_file):
        mock_gpio.set_garage_door.return_value = True

        actual = update_door_state(self.API_KEY, self.GARAGE_ID, self.REQUEST)

        assert actual.isGarageOpen == True

    def test_update_door_state__should_set_garage_door_to_requested_state(self, mock_gpio, mock_validate, mock_file):
        update_door_state(self.API_KEY, self.GARAGE_ID, self.REQUEST)

        mock_gpio.set_garage_door.assert_called_with(self.GARAGE_ID, True)

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

    def test_toggle_garage_door__should_not_update_door_duration(self, mock_gpio, mock_validate, mock_file):
        toggle_door(self.API_KEY, self.GARAGE_ID)

        mock_file.update_door_duration.assert_not_called()

    def test_update_door_state__should_not_update_door_duration_when_toggled(self, mock_gpio, mock_validate, mock_file):
        mock_gpio.is_garage_open.return_value = False

        update_door_state(self.API_KEY, self.GARAGE_ID, self.REQUEST)

        mock_file.update_door_duration.assert_not_called()

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


@patch('svc.controllers.garage_door_controller.DoorEvents')
@patch('svc.controllers.garage_door_controller.file_utils')
@patch('svc.controllers.garage_door_controller.validate_api_key')
@patch('svc.controllers.garage_door_controller.gpio_utils')
class TestStreamStatuses:
    API_KEY = 'fake_api_key'
    DURATION = datetime(2026, 1, 1, 12, 0, 0)

    def test_stream_statuses__should_validate_api_key_before_streaming(self, mock_gpio, mock_validate, mock_file, mock_events):
        mock_validate.side_effect = Unauthorized

        with pytest.raises(Unauthorized):
            stream_statuses(self.API_KEY)

    def test_stream_statuses__should_yield_status_event_first(self, mock_gpio, mock_validate, mock_file, mock_events):
        mock_file.get_door_duration.return_value = self.DURATION
        mock_gpio.is_garage_open.return_value = True
        mock_gpio.get_garage_coordinates.return_value = Coordinates({'Coordinates': {'latitude': 12.2, 'longitude': -94.23}})

        stream = stream_statuses(self.API_KEY)
        actual = next(stream)

        assert actual.startswith('event: status\ndata: ')
        assert actual.endswith('\n\n')
        payload = json.loads(actual.split('data: ', 1)[1])
        assert payload['coordinates'] == {'latitude': 12.2, 'longitude': -94.23}
        assert [door['garageId'] for door in payload['doors']] == ['1', '2']
        assert payload['doors'][0]['isGarageOpen'] is True
        assert payload['doors'][0]['duration'] == self.DURATION.isoformat()

    def test_stream_statuses__should_yield_ping_when_no_change_before_timeout(self, mock_gpio, mock_validate, mock_file, mock_events):
        mock_file.get_door_duration.return_value = self.DURATION
        mock_events.get_instance.return_value.wait_for_change.return_value = None

        stream = stream_statuses(self.API_KEY)
        next(stream)
        actual = next(stream)

        assert actual == ': ping\n\n'

    def test_stream_statuses__should_wait_with_heartbeat_timeout_from_current_version(self, mock_gpio, mock_validate, mock_file, mock_events):
        mock_file.get_door_duration.return_value = self.DURATION
        mock_events.get_instance.return_value.current_version.return_value = 7
        mock_events.get_instance.return_value.wait_for_change.return_value = None

        stream = stream_statuses(self.API_KEY)
        next(stream)
        next(stream)

        mock_events.get_instance.return_value.wait_for_change.assert_called_with(7, 20)

    def test_stream_statuses__should_yield_new_status_event_when_doors_change(self, mock_gpio, mock_validate, mock_file, mock_events):
        mock_file.get_door_duration.return_value = self.DURATION
        mock_events.get_instance.return_value.current_version.return_value = 0
        mock_events.get_instance.return_value.wait_for_change.side_effect = [1, None]
        mock_gpio.is_garage_open.side_effect = [False, False, True, False]

        stream = stream_statuses(self.API_KEY)
        next(stream)
        actual = next(stream)

        payload = json.loads(actual.split('data: ', 1)[1])
        assert payload['doors'][0]['isGarageOpen'] is True

    def test_stream_statuses__should_track_latest_version_after_change(self, mock_gpio, mock_validate, mock_file, mock_events):
        mock_file.get_door_duration.return_value = self.DURATION
        mock_events.get_instance.return_value.current_version.return_value = 0
        mock_events.get_instance.return_value.wait_for_change.side_effect = [3, None]

        stream = stream_statuses(self.API_KEY)
        next(stream)
        next(stream)
        next(stream)

        mock_events.get_instance.return_value.wait_for_change.assert_called_with(3, 20)
