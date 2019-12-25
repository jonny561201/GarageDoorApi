import json

from svc.utilities.gpio_utils import is_garage_open, update_garage_door, toggle_garage_door
from svc.utilities.jwt_utils import is_jwt_valid


# TODO: create thread to store and query status of door
def get_status(bearer_token):
    is_jwt_valid(bearer_token)
    status = is_garage_open()
    return {'isGarageOpen': status}


def update_state(bearer_token, request):
    is_jwt_valid(bearer_token)
    request_body = json.loads(request.decode('UTF-8'))
    new_state = update_garage_door(request_body)
    return {'garageDoorOpen': new_state}


def toggle_garage_door_state(bearer_token):
    is_jwt_valid(bearer_token)
    toggle_garage_door()
