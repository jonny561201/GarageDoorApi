# going to assume desired temperature is already converted to celsius by controller
from svc.constants.home_automation import HomeAutomation
from svc.utilities.gpio import read_temperature_file
from svc.utilities.temperature import get_user_temperature
from svc.utilities import gpio


class Hvac:
    def __init__(self, desired_temp, mode):
        self.DESIRED_TEMP = desired_temp
        self.MODE = mode

    def run_temperature_program(self):
        temp_file = read_temperature_file()
        celsius_temp = get_user_temperature(temp_file, False)

        if self.MODE == HomeAutomation.COOLING_MODE and celsius_temp > self.DESIRED_TEMP:
            gpio.turn_on_hvac(HomeAutomation.AC)
        elif self.MODE == HomeAutomation.HEATING_MODE and celsius_temp < self.DESIRED_TEMP:
            gpio.turn_on_hvac(HomeAutomation.FURNACE)
        else:
            device = HomeAutomation.AC if self.MODE == HomeAutomation.COOLING_MODE else HomeAutomation.FURNACE
            gpio.turn_off_hvac(device)
