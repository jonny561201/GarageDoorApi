from svc.utilities.gpio import read_temperature_file
from svc.utilities.temperature import get_user_temperature


def get_user_temp(user_id):
    temp_text = read_temperature_file()
    get_user_temperature(temp_text, False)
