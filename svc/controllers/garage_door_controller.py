import json
from datetime import datetime

import pytz

from svc.constants.garage_state import GarageState
from svc.services.garage_door import monitor_status
from svc.utilities import gpio_utils
from svc.utilities.event_utils import create_thread
from svc.utilities.jwt_utils import is_jwt_valid


def get_status(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    state = GarageState.get_instance()
    if state.ACTIVE_THREAD is None:
        create_thread(state, monitor_status)
        status = gpio_utils.is_garage_open()
        state.STATUS = status
        return {'isGarageOpen': status, 'statusDuration': datetime.now(pytz.utc)}
    else:
        return {'isGarageOpen': state.STATUS, 'statusDuration': state.OPEN_TIME if state.STATUS else state.CLOSED_TIME}


def update_state(bearer_token, garage_id, request):
    is_jwt_valid(bearer_token)
    request_body = json.loads(request.decode('UTF-8'))
    new_state = gpio_utils.update_garage_door(request_body)
    return {'garageDoorOpen': new_state}


def toggle_door(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    gpio_utils.toggle_garage_door()
