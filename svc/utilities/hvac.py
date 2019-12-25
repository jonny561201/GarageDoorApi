from svc.constants.home_automation import Automation
from svc.constants.hvac_state import HvacState
from svc.utilities import gpio
from svc.utilities.gpio import read_temperature_file
from svc.utilities.temperature_util import get_user_temperature


def run_temperature_program():
    temp_file = read_temperature_file()
    celsius_temp = get_user_temperature(temp_file, False)
    state = HvacState.get_instance()

    if state.MODE == Automation.MODE.COOLING and celsius_temp > state.DESIRED_TEMP:
        gpio.turn_on_hvac(Automation.HVAC.AIR_CONDITIONING)
    elif state.MODE == Automation.MODE.HEATING and celsius_temp < state.DESIRED_TEMP:
        gpio.turn_on_hvac(Automation.HVAC.FURNACE)
    else:
        gpio.turn_off_hvac(Automation.HVAC.AIR_CONDITIONING)
        gpio.turn_off_hvac(Automation.HVAC.FURNACE)
