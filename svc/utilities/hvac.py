# going to assume temperature is already converted to celsius by controller
from svc.utilities.gpio import read_temperature_file


def run_temperature_program(desired_temp):
    read_temperature_file()