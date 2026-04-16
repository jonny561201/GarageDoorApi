import RPi.GPIO as GPIO

from svc.constants.home_automation import Automation
from svc.manager import create_app, start_services


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Automation.GARAGE.FIRST_STATUS_PIN, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(Automation.GARAGE.SECOND_STATUS_PIN, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(Automation.GARAGE.FIRST_UPDATE_PIN, GPIO.OUT)
GPIO.setup(Automation.GARAGE.SECOND_UPDATE_PIN, GPIO.OUT)

GPIO.output(Automation.GARAGE.FIRST_UPDATE_PIN, GPIO.LOW)
GPIO.output(Automation.GARAGE.SECOND_UPDATE_PIN, GPIO.LOW)

app = create_app()
start_services(app)

if __name__ == '__main__':
    app.run()
