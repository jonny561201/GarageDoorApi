# import RPi.GPIO as GPIO
import time

from werkzeug.exceptions import BadRequest

from svc.constants.settings_state import Settings

FIRST_GARAGE_STATUS_PIN = 11
FIRST_GARAGE_STATE_PIN = 31

SECOND_GARAGE_STATUS_PIN = 12
SECOND_GARAGE_STATE_PIN = 33


# GPIO.cleanup()
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(FIRST_GARAGE_STATUS_PIN, GPIO.IN, GPIO.PUD_UP)
# GPIO.setup(SECOND_GARAGE_STATUS_PIN, GPIO.IN, GPIO.PUD_UP)
# GPIO.setup(FIRST_GARAGE_STATE_PIN, GPIO.OUT)
# GPIO.setup(SECOND_GARAGE_STATE_PIN, GPIO.OUT)

# GPIO.output(FIRST_GARAGE_STATE_PIN, GPIO.LOW)
# GPIO.output(SECOND_GARAGE_STATE_PIN, GPIO.LOW)


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


def toggle_garage_door(garage_id):
    pass
    # state_pin = FIRST_GARAGE_STATE_PIN if garage_id == '1' else SECOND_GARAGE_STATE_PIN
    # GPIO.output(state_pin, GPIO.HIGH)
    # time.sleep(.5)
    # GPIO.output(state_pin, GPIO.LOW)


def get_garage_coordinates():
    settings = Settings.get_instance()
    return settings.dev_coordinates
