import json

from mock import MagicMock, patch
from werkzeug.exceptions import BadRequest

from svc.controllers.door_queue_controller import update_door_worker


@patch('svc.controllers.door_queue_controller.schedule_utils')
@patch('svc.controllers.door_queue_controller.gpio_utils')
class TestUpdateDoorWorker:
    GARAGE_ID = '1'

    def _delivery(self):
        method = MagicMock()
        method.delivery_tag = 'tag'
        channel = MagicMock()
        return channel, method

    def _body(self, payload):
        return json.dumps(payload).encode('UTF-8')

    def test_schedule__should_delegate_to_schedule_utils(self, mock_gpio, mock_schedule):
        channel, method = self._delivery()
        payload = {'id': self.GARAGE_ID, 'action': 'schedule', 'delay_seconds': 300}
        body = self._body(payload)

        update_door_worker(channel, method, None, body)

        mock_schedule.schedule_close.assert_called_once_with(self.GARAGE_ID, payload)
        channel.basic_ack.assert_called_once_with(delivery_tag='tag')

    def test_toggle__should_toggle_garage_door(self, mock_gpio, mock_schedule):
        channel, method = self._delivery()
        body = self._body({'id': self.GARAGE_ID, 'action': 'toggle'})

        update_door_worker(channel, method, None, body)

        mock_gpio.toggle_garage_door.assert_called_once_with(self.GARAGE_ID)

    def test_schedule__should_nack_when_schedule_close_raises(self, mock_gpio, mock_schedule):
        channel, method = self._delivery()
        mock_schedule.schedule_close.side_effect = BadRequest
        body = self._body({'id': self.GARAGE_ID, 'action': 'schedule'})

        update_door_worker(channel, method, None, body)

        channel.basic_nack.assert_called_once_with(delivery_tag='tag', requeue=False)

    def test_update__should_set_garage_door_to_requested_state(self, mock_gpio, mock_schedule):
        channel, method = self._delivery()
        body = self._body({'id': self.GARAGE_ID, 'action': 'update', 'open': True})

        update_door_worker(channel, method, None, body)

        mock_gpio.set_garage_door.assert_called_once_with(self.GARAGE_ID, True)
        channel.basic_ack.assert_called_once_with(delivery_tag='tag')

    def test_update__should_nack_when_open_is_missing(self, mock_gpio, mock_schedule):
        channel, method = self._delivery()
        body = self._body({'id': self.GARAGE_ID, 'action': 'update'})

        update_door_worker(channel, method, None, body)

        mock_gpio.set_garage_door.assert_not_called()
        channel.basic_nack.assert_called_once_with(delivery_tag='tag', requeue=False)
