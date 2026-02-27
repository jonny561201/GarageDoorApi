import json

from svc.models.status import GarageStatus, GarageCoordinates
from svc.models.update import GarageUpdate
from svc.utilities import gpio_utils
from svc.utilities.file_utils import get_door_duration
from svc.utilities.jwt_utils import is_jwt_valid


def get_status(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    coordinates = gpio_utils.get_garage_coordinates()
    door_open = gpio_utils.is_garage_open(garage_id)
    duration = get_door_duration(garage_id)
    coordinates = GarageCoordinates(coordinates.latitude, coordinates.longitude)

    return GarageStatus(isGarageOpen=door_open, coordinates=coordinates, statusDuration=duration)


def update_state(bearer_token, garage_id, request):
    is_jwt_valid(bearer_token)
    request_body = json.loads(request.decode('UTF-8'))
    new_state = gpio_utils.update_garage_door(garage_id, request_body)
    return GarageUpdate(isGarageOpen=new_state)


def toggle_door(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    gpio_utils.toggle_garage_door(garage_id)


def update_door_worker(ch, method, properties, body: bytes):
    try:
        request = json.loads(body)
        garage_id = request.get('id')
        action = request.get('action')

        if action == 'toggle':
            gpio_utils.toggle_garage_door(garage_id)
        else:
            gpio_utils.update_garage_door(garage_id, request)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)