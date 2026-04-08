import json

from werkzeug.exceptions import BadRequest

from svc.models.status import GarageStatus, GarageCoordinates, GarageDoorStatus, AllGarageStatus
from svc.models.update import GarageUpdate
from svc.utilities import gpio_utils
from svc.utilities import file_utils
from svc.utilities.jwt_utils import is_jwt_valid


def get_status(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    coordinates = gpio_utils.get_garage_coordinates()
    door_open = gpio_utils.is_garage_open(garage_id)
    duration = file_utils.get_door_duration(garage_id)
    coordinates = GarageCoordinates(coordinates.latitude, coordinates.longitude)

    return GarageStatus(garageId=garage_id, isGarageOpen=door_open, coordinates=coordinates, statusDuration=duration)


def get_all_statuses(bearer_token):
    is_jwt_valid(bearer_token)
    raw_coordinates = gpio_utils.get_garage_coordinates()
    coordinates = GarageCoordinates(raw_coordinates.latitude, raw_coordinates.longitude)

    garage_ids = ['1', '2']
    doors = []
    for garage_id in garage_ids:
        door_open = gpio_utils.is_garage_open(garage_id)
        duration = file_utils.get_door_duration(garage_id)
        doors.append(GarageDoorStatus(garageId=garage_id, isGarageOpen=door_open, statusDuration=duration))

    return AllGarageStatus(coordinates=coordinates, doors=doors)


def update_door_state(bearer_token: str, garage_id: str, request):
    is_jwt_valid(bearer_token)
    request_body = json.loads(request.decode('UTF-8'))
    status = _update_garage_door(garage_id, request_body)

    return GarageUpdate(isGarageOpen=status)


def toggle_door(bearer_token, garage_id):
    is_jwt_valid(bearer_token)
    gpio_utils.toggle_garage_door(garage_id)
    file_utils.update_door_duration(garage_id)


def update_door_worker(ch, method, properties, body: bytes):
    try:
        request = json.loads(body)
        garage_id = request.get('id')
        action = request.get('action')

        if action == 'toggle':
            gpio_utils.toggle_garage_door(garage_id)
        else:
            _update_garage_door(garage_id, request)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def _update_garage_door(garage_id: str, request: dict):
    try:
        status = gpio_utils.is_garage_open(garage_id)
        if request['open'] != status:
            gpio_utils.toggle_garage_door(garage_id)
            file_utils.update_door_duration(garage_id)
            return not status
    except KeyError:
        raise BadRequest

    return status
