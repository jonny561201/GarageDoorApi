import re

from werkzeug.exceptions import Conflict


def get_temperature(temp_text, isFahrenheit):
    if temp_text[0][-3:] != 'YES':
        raise Conflict
    temp_string = re.search('(t=\d*)', temp_text[1])
    if temp_string is None:
        raise Conflict

    celsius = _get_celsius_value(temp_string.group())
    return _convert_temp(celsius, isFahrenheit)


def _get_celsius_value(temp_row):
    cleaned_text = temp_row.replace('t=', '')
    temp_celsius = int(cleaned_text)
    return round(temp_celsius / 1000, 2)


def _convert_temp(celsius, isFahrenheit):
    if isFahrenheit:
        return celsius * 1.8 + 32
    return celsius
