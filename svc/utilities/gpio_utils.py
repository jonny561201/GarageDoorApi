# import RPi.GPIO as GPIO

from werkzeug.exceptions import BadRequest

from svc.config.settings_state import Settings
from svc.constants.home_automation import Automation


# assumes connection to output pin and ground with GPIO.PUD_UP
def is_garage_open(garage_id):
    return True
    # status_pin = FIRST_GARAGE_STATUS_PIN if garage_id == '1' else SECOND_GARAGE_STATUS_PIN
    # status = GPIO.input(status_pin)
    # return True if status == 1 else False


# return true for open and false for closed
def update_garage_door(garage_id, requested_state):
    try:
        status = is_garage_open(garage_id)
        if requested_state['garageDoorOpen'] != status:
            toggle_garage_door(garage_id)
    except KeyError:
        raise BadRequest
    return not status


def update_garage_door_v2(garage_id, requested_state):
    try:
        status = is_garage_open(garage_id)
        if requested_state['open'] != status:
            toggle_garage_door(garage_id)
    except KeyError:
        raise BadRequest
    return not status


def toggle_garage_door(garage_id):
    pass
    # state_pin = FIRST_GARAGE_STATE_PIN if garage_id == '1' else SECOND_GARAGE_STATE_PIN
    # GPIO.output(state_pin, GPIO.HIGH)
    # time.sleep(.5)
    # GPIO.output(state_pin, GPIO.LOW)


def get_garage_coordinates():
    settings = Settings.get_instance()
    return settings.Coordinates
