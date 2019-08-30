import re

from werkzeug.exceptions import Conflict

from svc.utilities.gpio import read_temperature_file


def get_temperature():
    temp_file_results = read_temperature_file()
    if temp_file_results[0][-3:] != 'YES':
        raise Conflict
    return _get_temp_value(temp_file_results[1])


def _get_temp_value(temp_row):
    temp_text = re.search('(t=\d*)', temp_row).group()

    cleaned_text = temp_text.replace('t=', '')
    temp_celsius = int(cleaned_text)
    return round(temp_celsius / 1000, 2)
