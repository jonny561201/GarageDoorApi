# going to assume temperature is already converted to celsius by controller
from svc.utilities.gpio import read_temperature_file
from svc.utilities.temperature import get_user_temperature


def run_temperature_program(desired_temp):
    read_temperature_file()
    get_user_temperature()