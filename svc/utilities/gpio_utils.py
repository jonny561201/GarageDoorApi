# import RPi.GPIO as GPIO

from werkzeug.exceptions import BadRequest

GARAGE_STATUS_PIN = 7
GARAGE_STATE_PIN = 8
# TODO: find the correct pins to use


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
    except KeyError:
        raise BadRequest
    return True
    # status = garage_door_status()
    # if requested_state['garageDoorOpen'] is True and status is False:
    #     toggle_garage_door()


def toggle_garage_door():
    pass
    #     GPIO.output(GARAGE_STATE_PIN, GPIO.LOW)
    #     time.sleep(.5)
    #     GPIO.output(GARAGE_STATE_PIN, GPIO.HIGH)

