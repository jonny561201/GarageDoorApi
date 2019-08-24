# import RPi.GPIO as GPIO


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


def update_garage_door(requested_state):
    pass
    # status = garage_door_status()
    # if requested_state['openGarageDoor'] is True and status['isGarageOpen'] is True:
    #     GPIO.setup(OUTPUT_PIN, GPIO.HIGH)
    #     GPIO.cleanup()
