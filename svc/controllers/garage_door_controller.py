import json

from svc.utilities import gpio_utils
from svc.utilities.file_utils import get_door_duration
from svc.utilities.jwt_utils import is_jwt_valid


def get_status(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    return {'isGarageOpen': gpio_utils.is_garage_open(garage_id),
            'statusDuration': get_door_duration(garage_id),
            'coordinates': gpio_utils.get_garage_coordinates()}


def update_state(bearer_token, garage_id, request):
    is_jwt_valid(bearer_token)
    request_body = json.loads(request.decode('UTF-8'))
    new_state = gpio_utils.update_garage_door(garage_id, request_body)
    return {'isGarageOpen': new_state}


def toggle_door(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    gpio_utils.toggle_garage_door(garage_id)
