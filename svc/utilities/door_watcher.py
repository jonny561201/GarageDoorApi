import threading
import time

from svc.config.door_events import DoorEvents
from svc.constants.home_automation import Garage
from svc.utilities import file_utils
from svc.utilities import gpio_utils


def start_door_watcher():
    thread = threading.Thread(target=_watch_doors, daemon=True)
    thread.start()


def poll_doors(previous_states):
    current_states = {garage_id: gpio_utils.is_garage_open(garage_id) for garage_id in Garage.DOOR_IDS}
    if len(previous_states) == 0:
        return current_states
    changed_ids = [garage_id for garage_id in Garage.DOOR_IDS if current_states[garage_id] != previous_states.get(garage_id)]
    for garage_id in changed_ids:
        file_utils.update_door_duration(garage_id)
    if len(changed_ids) > 0:
        DoorEvents.get_instance().notify()
    return current_states


def _watch_doors():
    states = {}
    while True:
        states = poll_doors(states)
        time.sleep(Garage.WATCH_INTERVAL_SECONDS)
