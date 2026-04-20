from mock import MagicMock

from svc.config.sessions import Session


class TestSession:
    DOOR_ID = '1'

    def setup_method(self):
        Session._instance = None
        self.session = Session.get_instance()

    def test_set_timer__should_cancel_existing_timer_when_replacing(self):
        first = MagicMock()
        second = MagicMock()
        self.session.set_timer(self.DOOR_ID, first)

        self.session.set_timer(self.DOOR_ID, second)

        first.cancel.assert_called_once()
        second.cancel.assert_not_called()

    def test_clear_timer__should_cancel_and_return_true(self):
        timer = MagicMock()
        self.session.set_timer(self.DOOR_ID, timer)

        result = self.session.clear_timer(self.DOOR_ID)

        timer.cancel.assert_called_once()
        assert result is True

    def test_clear_timer__should_return_false_when_no_timer(self):
        assert self.session.clear_timer(self.DOOR_ID) is False

    def test_clear_timer__should_be_idempotent(self):
        timer = MagicMock()
        self.session.set_timer(self.DOOR_ID, timer)

        self.session.clear_timer(self.DOOR_ID)

        assert self.session.clear_timer(self.DOOR_ID) is False

    def test_set_timer__isolates_doors(self):
        timer_one = MagicMock()
        timer_two = MagicMock()

        self.session.set_timer('1', timer_one)
        self.session.set_timer('2', timer_two)

        timer_one.cancel.assert_not_called()
        timer_two.cancel.assert_not_called()
