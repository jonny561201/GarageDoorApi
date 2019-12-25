import os

from svc.services.weather_request import get_weather
from svc.utilities.gpio import read_temperature_file
from svc.utilities.temperature_util import get_user_temperature


def get_external_temp(preference):
    temp_unit = "metric" if preference['temp_unit'] == "celsius" else "imperial"
    weather_data = get_weather(preference['city'], temp_unit, 'bdeb14f537691e6266ed3023605f72a5')
    return weather_data


def get_internal_temp(preference):
    temp_text = read_temperature_file()
    return get_user_temperature(temp_text, preference['is_fahrenheit'])
