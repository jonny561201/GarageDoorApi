# import RPi.GPIO as GPIO
# import time

from werkzeug.exceptions import BadRequest

INPUT_PIN = 7
OUTPUT_PIN = 8


# GPIO.cleanup()
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(INPUT_PIN, GPIO.IN, GPIO.PUD_UP)
# GPIO.setup(OUTPUT_PIN, GPIO.OUT)


# assumes connection to output pin and ground with GPIO.PUD_UP
def garage_door_status():
    return True
    # status = GPIO.input(INPUT_PIN)
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
    #     GPIO.output(OUTPUT_PIN, GPIO.LOW)
    #     time.sleep(.5)
    #     GPIO.output(OUTPUT_PIN, GPIO.HIGH)


def read_temperature_file():
    return ['72 01 4b 46 7f ff 0e 10 57 : crc=57 YES',
            '72 01 4b 46 7f ff 0e 10 57 t=23125']