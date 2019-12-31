from datetime import datetime

import pytz

from svc.constants.garage_state import GarageState
from svc.constants.home_automation import Automation
from svc.utilities.gpio_utils import is_garage_open


def monitor_status():
    status = is_garage_open()
    state = GarageState.get_instance()

    if status and state.OPEN_TIME is None:
        state.STATUS = Automation.GARAGE.OPEN
        state.OPEN_TIME = datetime.now(pytz.utc)
        state.CLOSED_TIME = None
    if not status and state.CLOSED_TIME is None:
        state.STATUS = Automation.GARAGE.CLOSED
        state.CLOSED_TIME = datetime.now(pytz.utc)
        state.OPEN_TIME = None
