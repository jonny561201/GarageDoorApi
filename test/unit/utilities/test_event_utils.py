from threading import Event

from mock import patch, create_autospec, Mock

from svc.constants.garage_state import GarageState
from svc.utilities.event_utils import create_thread, MyThread


@patch('svc.utilities.event_utils.MyThread')
@patch('svc.utilities.event_utils.Event')
class TestEvent:
    STATE = None
    FUNCT = print

    def setup_method(self):
        self.STATE = GarageState.get_instance()

    def test_create_thread__should_set_stop_event(self, mock_event, mock_thread):
        event = Event()
        mock_event.return_value = event
        create_thread(self.STATE, self.FUNCT)

        assert self.STATE.STOP_EVENT == event

    def test_create_thread__should_set_active_thread(self, mock_event, mock_thread):
        thread = create_autospec(MyThread)
        mock_thread.return_value = thread
        create_thread(self.STATE, self.FUNCT)

        assert self.STATE.ACTIVE_THREAD == thread

    def test_create_thread__should_start_the_active_thread(self, mock_event, mock_thread):
        thread = Mock()
        mock_thread.return_value = thread
        create_thread(self.STATE, self.FUNCT)

        thread.start.assert_called()
