# if garage door status open and open time null set open time and status
# if garage door status closed and closed time null set closed time and status
from datetime import datetime

from svc.constants.garage_state import GarageState
from svc.constants.home_automation import Automation
from svc.utilities.gpio import is_garage_open


def monitor_status():
    status = is_garage_open()
    state = GarageState.get_instance()

    if status:
        state.STATUS = Automation.GARAGE.OPEN
        state.OPEN_TIME = datetime.now()
    if not status:
        state.STATUS = Automation.GARAGE.CLOSED
