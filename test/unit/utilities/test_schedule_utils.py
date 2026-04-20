import pytest
from mock import MagicMock, patch
from werkzeug.exceptions import BadRequest

from svc.utilities import schedule_utils


@patch('svc.utilities.schedule_utils.file_utils')
@patch('svc.utilities.schedule_utils.gpio_utils')
@patch('svc.utilities.schedule_utils.Session')
@patch('svc.utilities.schedule_utils.threading.Timer')
class TestScheduleClose:
    GARAGE_ID = '1'

    def test_should_create_daemon_timer_with_delay(self, mock_timer_cls, mock_session, mock_gpio, mock_file):
        schedule_utils.schedule_close(self.GARAGE_ID, {'delay_seconds': 60})

        mock_timer_cls.assert_called_once()
        assert mock_timer_cls.call_args.args[0] == 60.0
        assert mock_timer_cls.return_value.daemon is True

    def test_should_register_and_start_timer(self, mock_timer_cls, mock_session, mock_gpio, mock_file):
        schedule_utils.schedule_close(self.GARAGE_ID, {'delay_seconds': 60})

        mock_session.get_instance.return_value.set_timer.assert_called_once_with(
            self.GARAGE_ID, mock_timer_cls.return_value
        )
        mock_timer_cls.return_value.start.assert_called_once()

    def test_should_raise_bad_request_when_delay_missing(self, mock_timer_cls, mock_session, mock_gpio, mock_file):
        with pytest.raises(BadRequest):
            schedule_utils.schedule_close(self.GARAGE_ID, {})

        mock_timer_cls.assert_not_called()

    def test_fire__closes_open_door_and_clears_session(self, mock_timer_cls, mock_session, mock_gpio, mock_file):
        mock_gpio.is_garage_open.return_value = True
        schedule_utils.schedule_close(self.GARAGE_ID, {'delay_seconds': 60})

        fire = mock_timer_cls.call_args.args[1]
        fire()

        mock_session.get_instance.return_value.clear_timer.assert_called_once_with(self.GARAGE_ID)
        mock_gpio.toggle_garage_door.assert_called_once_with(self.GARAGE_ID)
        mock_file.update_door_duration.assert_called_once_with(self.GARAGE_ID)

    def test_fire__does_not_toggle_when_already_closed(self, mock_timer_cls, mock_session, mock_gpio, mock_file):
        mock_gpio.is_garage_open.return_value = False
        schedule_utils.schedule_close(self.GARAGE_ID, {'delay_seconds': 60})

        fire = mock_timer_cls.call_args.args[1]
        fire()

        mock_session.get_instance.return_value.clear_timer.assert_called_once_with(self.GARAGE_ID)
        mock_gpio.toggle_garage_door.assert_not_called()
        mock_file.update_door_duration.assert_not_called()


@patch('svc.utilities.schedule_utils.Session')
class TestCancel:
    GARAGE_ID = '1'

    def test_cancel__returns_session_clear_result(self, mock_session):
        mock_session.get_instance.return_value.clear_timer.return_value = True

        assert schedule_utils.cancel(self.GARAGE_ID) is True
        mock_session.get_instance.return_value.clear_timer.assert_called_once_with(self.GARAGE_ID)

    def test_cancel__returns_false_when_nothing_to_cancel(self, mock_session):
        mock_session.get_instance.return_value.clear_timer.return_value = False

        assert schedule_utils.cancel(self.GARAGE_ID) is False
