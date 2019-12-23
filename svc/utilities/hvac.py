from svc.constants.home_automation import Automation
from svc.constants.hvac_state import HvacState
from svc.utilities import gpio
from svc.utilities.gpio import read_temperature_file
from svc.utilities.temperature import get_user_temperature


def run_temperature_program():
    temp_file = read_temperature_file()
    celsius_temp = get_user_temperature(temp_file, False)
    state = HvacState.get_instance()

    if state.MODE == Automation.COOLING_MODE and celsius_temp > state.DESIRED_TEMP:
        gpio.turn_on_hvac(Automation.AIR_CONDITIONING)
    elif state.MODE == Automation.HEATING_MODE and celsius_temp < state.DESIRED_TEMP:
        gpio.turn_on_hvac(Automation.FURNACE)
    else:
        device = Automation.AIR_CONDITIONING if state.MODE == Automation.COOLING_MODE else Automation.FURNACE
        gpio.turn_off_hvac(device)
