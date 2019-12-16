import re

from werkzeug.exceptions import Conflict


def get_user_temperature(temp_text, is_fahrenheit):
    if temp_text[0][-3:] != 'YES':
        raise Conflict
    temp_string = re.search('(t=\d*)', temp_text[1])
    if temp_string is None:
        raise Conflict

    celsius = _get_celsius_value(temp_string.group())
    return _convert_to_correct_unit(celsius, is_fahrenheit)


def convert_to_fahrenheit(celsius_temp):
    return celsius_temp * 1.8 + 32


def convert_to_celsius(fahrenheit_temp):
    return round((fahrenheit_temp - 32) / 1.8, 2)


def _get_celsius_value(temp_row):
    cleaned_text = temp_row.replace('t=', '')
    temp_celsius = int(cleaned_text)
    return round(temp_celsius / 1000, 2)


def _convert_to_correct_unit(celsius, is_fahrenheit):
    if is_fahrenheit:
        return convert_to_fahrenheit(celsius)
    return celsius
