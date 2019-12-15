# going to assume desired temperature is already converted to celsius by controller
from svc.constants.home_automation import HomeAutomation
from svc.utilities.gpio import read_temperature_file
from svc.utilities.temperature import get_user_temperature
from svc.utilities import gpio


def run_temperature_program(desired_temp, mode):
    temp_file = read_temperature_file()
    celsius_temp = get_user_temperature(temp_file, False)

    if mode == HomeAutomation.COOLING_MODE and celsius_temp > desired_temp:
        gpio.turn_on_hvac(HomeAutomation.AC)
    elif mode == HomeAutomation.HEATING_MODE and celsius_temp < desired_temp:
        gpio.turn_on_hvac(HomeAutomation.FURNACE)
    elif mode == HomeAutomation.HEATING_MODE:
        gpio.turn_off_hvac(HomeAutomation.FURNACE)
    elif mode == HomeAutomation.COOLING_MODE:
        gpio.turn_off_hvac(HomeAutomation.AC)
