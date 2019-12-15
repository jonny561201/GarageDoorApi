# import RPi.GPIO as GPIO
# import time

from werkzeug.exceptions import BadRequest

GARAGE_STATUS_PIN = 7
GARAGE_STATE_PIN = 8
# TODO: find the correct pins to use
AC_PIN = 23
HEAT_PIN = 26


# GPIO.cleanup()
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(GARAGE_STATUS_PIN, GPIO.IN, GPIO.PUD_UP)
# GPIO.setup(GARAGE_STATE_PIN, GPIO.OUT)
# GPIO.setup(AC_PIN, GPIO.OUT)
# GPIO.setup(HEAT_PIN, GPIO.OUT)


# assumes connection to output pin and ground with GPIO.PUD_UP
def garage_door_status():
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


def read_temperature_file():
    return ['72 01 4b 46 7f ff 0e 10 57 : crc=57 YES',
            '72 01 4b 46 7f ff 0e 10 57 t=23125']


def turn_on_hvac(device):
     # if device == 'ac':
     #     GPIO.output(AC_PIN, GPIO.LOW)
     # else:
     #     GPIO.output(HEAT_PIN, GPIO.LOW)
     pass


def turn_off_hvac(device):
    # if device == 'ac':
    #     GPIO.output(AC_PIN, GPIO.HIGH)
    # else:
    #     GPIO.output(HEAT_PIN, GPIO.HIGH)
    pass
