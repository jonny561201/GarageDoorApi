import json
from datetime import datetime
from threading import Event

import pytz

from svc.constants.garage_state import GarageState
from svc.constants.home_automation import Automation
from svc.services.garage_door import monitor_status
from svc.utilities.event_utils import MyThread
from svc.utilities import gpio_utils
from svc.utilities.jwt_utils import is_jwt_valid


def get_status(bearer_token):
    is_jwt_valid(bearer_token)
    state = GarageState.get_instance()
    if state.ACTIVE_THREAD is None:
        __create_thread(state)
        return {'isGarageOpen': gpio_utils.is_garage_open(), 'statusDuration': datetime.now(pytz.utc)}
    else:
        return {'isGarageOpen': state.STATUS, 'statusDuration': state.OPEN_TIME if state.STATUS else state.CLOSED_TIME}


def update_state(bearer_token, request):
    is_jwt_valid(bearer_token)
    request_body = json.loads(request.decode('UTF-8'))
    new_state = gpio_utils.update_garage_door(request_body)
    return {'garageDoorOpen': new_state}


def toggle_garage_door_state(bearer_token):
    is_jwt_valid(bearer_token)
    gpio_utils.toggle_garage_door()


def __create_thread(state):
    stop_event = Event()
    state.STOP_EVENT = stop_event
    state.ACTIVE_THREAD = MyThread(stop_event, monitor_status, Automation.TIME.THIRTY_SECONDS)
    state.ACTIVE_THREAD.start()
