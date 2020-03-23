# import RPi.GPIO as GPIO
import time

from werkzeug.exceptions import BadRequest

GARAGE_STATUS_PIN = 11
GARAGE_STATE_PIN = 7


# GPIO.cleanup()
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(GARAGE_STATUS_PIN, GPIO.IN, GPIO.PUD_UP)
# GPIO.setup(GARAGE_STATE_PIN, GPIO.OUT)


# assumes connection to output pin and ground with GPIO.PUD_UP
def is_garage_open():
    return True
    # status = GPIO.input(GARAGE_STATUS_PIN)
    # return True if status == 1 else False


# return true for open and false for closed
def update_garage_door(requested_state):
    try:
        requested_state['garageDoorOpen']
        # status = is_garage_open()
        # if requested_state['garageDoorOpen'] != status:
        #     toggle_garage_door()
    except KeyError:
        raise BadRequest
    return True


def toggle_garage_door():
    pass
    # GPIO.output(GARAGE_STATE_PIN, GPIO.LOW)
    # time.sleep(.2)
    # GPIO.output(GARAGE_STATE_PIN, GPIO.HIGH)

