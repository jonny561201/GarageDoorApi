# going to assume temperature is already converted to celsius by controller
from svc.constants.home_automation import HomeAutomation
from svc.utilities.gpio import read_temperature_file
from svc.utilities.temperature import get_user_temperature
from svc.utilities import gpio


def run_temperature_program(desired_temp):
    temp_file = read_temperature_file()
    get_user_temperature(temp_file, False)

    gpio.turn_on_hvac(HomeAutomation.AC)