import json

from svc.constants.garage_state import GarageState
from svc.services.garage_door import monitor_status
from svc.utilities import gpio_utils
from svc.utilities.event_utils import create_thread
from svc.utilities.jwt_utils import is_jwt_valid


def get_status(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    state = GarageState.get_instance().DOORS[garage_id]
    if state.ACTIVE_THREAD is None:
        create_thread(state, lambda: monitor_status(state, garage_id))
    return {'isGarageOpen': state.STATUS,
            'statusDuration': state.OPEN_TIME if state.STATUS else state.CLOSED_TIME,
            'coordinates': gpio_utils.get_garage_coordinates()}


def update_state(bearer_token, garage_id, request):
    is_jwt_valid(bearer_token)
    request_body = json.loads(request.decode('UTF-8'))
    new_state = gpio_utils.update_garage_door(garage_id, request_body)
    return {'garageDoorOpen': new_state}


def toggle_door(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    gpio_utils.toggle_garage_door(garage_id)
