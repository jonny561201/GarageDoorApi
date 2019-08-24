# import RPi.GPIO as GPIO
from werkzeug.exceptions import BadRequest

INPUT_PIN = 7
OUTPUT_PIN = 8
# GPIO.setmode(GPIO.BOARD)


# assumes connection to output pin and ground with GPIO.PUD_UP
def garage_door_status():
    return {'isGarageOpen': True}
    # GPIO.setup(INPUT_PIN, GPIO.IN, GPIO.PUD_UP)
    #
    # status = GPIO.input(INPUT_PIN)
    # GPIO.cleanup()
    #
    # return {'isGarageOpen': True if status == 1 else False}


# return true for open and false for closed
def update_garage_door(requested_state):
    try:
        requested_state['garageDoorOpen']
    except KeyError:
        raise BadRequest
    return True
    # status = garage_door_status()
    # if requested_state['garageDoorOpen'] is True and status['isGarageOpen'] is False:
    #     GPIO.setup(OUTPUT_PIN, GPIO.HIGH)
    #     GPIO.cleanup()
