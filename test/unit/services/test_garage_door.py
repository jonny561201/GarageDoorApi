from datetime import datetime, timedelta

import pytz
from mock import patch

from svc.constants.garage_state import GarageState
from svc.constants.home_automation import Automation
from svc.services.garage_door import monitor_status


@patch('svc.services.garage_door.datetime')
@patch('svc.services.garage_door.is_garage_open')
class TestGarageService:

    GARAGE_ID = 3
    DATE = datetime.now(pytz.utc)
    STATE = GarageState.get_instance()

    def setup_method(self):
        self.STATE.CLOSED_TIME = None
        self.STATE.OPEN_TIME = None
        self.STATE.STATUS = None

    def test_monitor_status__should_call_is_garage_open(self, mock_status, mock_date):
        monitor_status(self.GARAGE_ID)

        mock_status.assert_called_with(self.GARAGE_ID)

    def test_monitor_status__should_set_status_to_open_when_garage_open(self, mock_status, mock_date):
        mock_status.return_value = True

        monitor_status(self.GARAGE_ID)

        assert self.STATE.STATUS == Automation.GARAGE.OPEN

    def test_monitor_status__should_set_open_time_when_garage_open(self, mock_status, mock_date):
        mock_status.return_value = True
        mock_date.now.return_value = self.DATE

        monitor_status(self.GARAGE_ID)

        assert self.STATE.OPEN_TIME == self.DATE

    def test_monitor_status__should_set_status_to_closed_when_garage_door_closed(self, mock_status, mock_date):
        mock_status.return_value = False

        monitor_status(self.GARAGE_ID)

        assert self.STATE.STATUS == Automation.GARAGE.CLOSED

    def test_monitor_status__should_set_closed_time_when_garage_closed(self, mock_status, mock_date):
        mock_status.return_value = False
        mock_date.now.return_value = self.DATE

        monitor_status(self.GARAGE_ID)

        assert self.STATE.CLOSED_TIME == self.DATE

    def test_monitor_status__should_nullify_open_date_when_closed(self, mock_status, mock_date):
        mock_status.return_value = False

        monitor_status(self.GARAGE_ID)

        assert self.STATE.OPEN_TIME is None

    def test_monitor_status__should_nullify_closed_date_when_opened(self, mock_status, mock_date):
        mock_status.return_value = True

        monitor_status(self.GARAGE_ID)

        assert self.STATE.CLOSED_TIME is None

    def test_monitor_status__should_not_reset_open_date_when_already_open(self, mock_status, mock_date):
        older_date = datetime.now() - timedelta(days=1)
        mock_status.return_value = True
        mock_date.now.return_value = self.DATE
        self.STATE.OPEN_TIME = older_date

        monitor_status(self.GARAGE_ID)

        assert self.STATE.OPEN_TIME == older_date

    def test_monitor_status__should_not_reset_closed_date_when_already_closed(self, mock_status, mock_date):
        older_date = datetime.now() - timedelta(days=1)
        mock_status.return_value = False
        mock_date.now.return_value = self.DATE
        self.STATE.CLOSED_TIME = older_date

        monitor_status(self.GARAGE_ID)

        assert self.STATE.CLOSED_TIME == older_date
