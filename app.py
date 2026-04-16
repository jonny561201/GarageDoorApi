import RPi.GPIO as GPIO

from svc.constants.home_automation import Garage
from svc.manager import create_app, start_services


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Garage.FIRST_STATUS_PIN, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(Garage.SECOND_STATUS_PIN, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(Garage.FIRST_UPDATE_PIN, GPIO.OUT)
GPIO.setup(Garage.SECOND_UPDATE_PIN, GPIO.OUT)

GPIO.output(Garage.FIRST_UPDATE_PIN, GPIO.LOW)
GPIO.output(Garage.SECOND_UPDATE_PIN, GPIO.LOW)

app = create_app()
start_services(app)

if __name__ == '__main__':
    app.run()
