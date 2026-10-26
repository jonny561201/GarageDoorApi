import json

from werkzeug.exceptions import BadRequest

from svc.config.door_events import DoorEvents
from svc.constants.home_automation import Garage
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
    return _build_all_statuses()


def stream_statuses(api_key):
    validate_api_key(api_key)
    return _status_stream()


def update_door_state(api_key: str, garage_id: str, request):
    validate_api_key(api_key)
    request_body = json.loads(request.decode('UTF-8'))
    try:
        status = gpio_utils.set_garage_door(garage_id, request_body['open'])
    except KeyError:
        raise BadRequest

    return GarageUpdate(isGarageOpen=status)


def toggle_door(api_key, garage_id):
    validate_api_key(api_key)
    gpio_utils.toggle_garage_door(garage_id)


def cancel_schedule(api_key, garage_id):
    validate_api_key(api_key)
    return {'cancelled': schedule_utils.cancel(garage_id)}


def _build_all_statuses():
    raw_coordinates = gpio_utils.get_garage_coordinates()
    coordinates = GarageCoordinates(raw_coordinates.latitude, raw_coordinates.longitude)
    doors = [_create_door_status(garage_id) for garage_id in Garage.DOOR_IDS]

    return AllGarageStatus(coordinates=coordinates, doors=doors)


def _status_stream():
    events = DoorEvents.get_instance()
    seen_version = events.current_version()
    yield _format_status_event()
    while True:
        version = events.wait_for_change(seen_version, Garage.STREAM_HEARTBEAT_SECONDS)
        if version is None:
            yield ': ping\n\n'
        else:
            seen_version = version
            yield _format_status_event()


def _format_status_event():
    return f'event: status\ndata: {_build_all_statuses().to_json()}\n\n'


def _create_door_status(garage_id):
    door_open = gpio_utils.is_garage_open(garage_id)
    duration = file_utils.get_door_duration(garage_id)
    return GarageDoorStatus(garageId=garage_id, isGarageOpen=door_open, duration=duration)
