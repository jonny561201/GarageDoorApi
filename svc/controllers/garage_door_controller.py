import json

from svc.utilities.gpio import garage_door_status, update_garage_door
from svc.utilities.jwt_utils import is_jwt_valid


def get_status(bearer_token):
    is_jwt_valid(bearer_token)
    status = garage_door_status()
    return {'isGarageOpen': status}


def update_state(bearer_token, request):
    is_jwt_valid(bearer_token)
    request_body = request.decode('UTF-8')
    new_state = update_garage_door(json.loads(request_body))
    return {'garageDoorOpen': new_state}
