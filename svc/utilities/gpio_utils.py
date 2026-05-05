import time
import random

# import RPi.GPIO as GPIO

from svc.config.settings_state import Settings
from svc.constants.home_automation import Garage


# assumes connection to output pin and ground with GPIO.PUD_UP
def is_garage_open(garage_id):
    return bool(random.getrandbits(1))
    # status_pin = Garage.FIRST_STATUS_PIN if garage_id == '1' else Garage.SECOND_STATUS_PIN
    # status = GPIO.input(status_pin)
    # return True if status == 1 else False


def toggle_garage_door(garage_id):
    pass
    # state_pin = Garage.FIRST_UPDATE_PIN if garage_id == '1' else Garage.SECOND_UPDATE_PIN
    # GPIO.output(state_pin, GPIO.HIGH)
    # time.sleep(.5)
    # GPIO.output(state_pin, GPIO.LOW)


def get_garage_coordinates():
    settings = Settings.get_instance()
    return settings.Coordinates
