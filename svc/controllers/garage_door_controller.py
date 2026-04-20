import json

from werkzeug.exceptions import BadRequest

from svc.models.status import GarageStatus, GarageCoordinates, GarageDoorStatus, AllGarageStatus
from svc.models.update import GarageUpdate
from svc.utilities import gpio_utils
from svc.utilities import file_utils
from svc.utilities import schedule_utils
from svc.utilities.api_key_utils import validate_api_key


def get_status(api_key, garage_id):
    validate_api_key(api_key)
    coordinates = gpio_utils.get_garage_coordinates()
    door_open = gpio_utils.is_garage_open(garage_id)
    duration = file_utils.get_door_duration(garage_id)
    coordinates = GarageCoordinates(coordinates.latitude, coordinates.longitude)

    return GarageStatus(garageId=garage_id, isGarageOpen=door_open, coordinates=coordinates, duration=duration)


def get_all_statuses(api_key):
    validate_api_key(api_key)
    raw_coordinates = gpio_utils.get_garage_coordinates()
    coordinates = GarageCoordinates(raw_coordinates.latitude, raw_coordinates.longitude)

    garage_ids = ['1', '2']
    doors = [_create_door_status(garage_id) for garage_id in garage_ids]

    return AllGarageStatus(coordinates=coordinates, doors=doors)


def update_door_state(api_key: str, garage_id: str, request):
    validate_api_key(api_key)
    request_body = json.loads(request.decode('UTF-8'))
    status = _update_garage_door(garage_id, request_body)

    return GarageUpdate(isGarageOpen=status)


def toggle_door(api_key, garage_id):
    validate_api_key(api_key)
    gpio_utils.toggle_garage_door(garage_id)
    file_utils.update_door_duration(garage_id)


def cancel_schedule(api_key, garage_id):
    validate_api_key(api_key)
    return {'cancelled': schedule_utils.cancel(garage_id)}


def update_door_worker(ch, method, properties, body: bytes):
    try:
        request = json.loads(body)
        garage_id = request.get('id')
        action = request.get('action')

        if action == 'toggle':
            gpio_utils.toggle_garage_door(garage_id)
            file_utils.update_door_duration(garage_id)
        elif action == 'update':
            _update_garage_door(garage_id, request)
        elif action == 'schedule':
            schedule_utils.schedule_close(garage_id, request)

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


def _create_door_status(garage_id):
    door_open = gpio_utils.is_garage_open(garage_id)
    duration = file_utils.get_door_duration(garage_id)
    return GarageDoorStatus(garageId=garage_id, isGarageOpen=door_open, duration=duration)
