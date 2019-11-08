import json

import requests
from werkzeug.exceptions import Unauthorized, BadRequest


def get_weather_by_city(city, unit_preference, app_id):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    args = {'q': city,
            'units': unit_preference,
            'APPID': app_id}
    response = requests.get(base_url, params=args)
    __validate_response(response)
    response_content = json.loads(response.content)
    temp_response = __build_response(response_content)

    return temp_response


def __validate_response(response):
    if response.status_code == 401:
        raise Unauthorized
    if not response.ok:
        raise BadRequest


def __build_response(response_content):
    current_temp = response_content['main'].get('temp', 0.0)
    min_temp = response_content['main'].get('temp_min', 0.0)
    max_temp = response_content['main'].get('temp_max', 0.0)
    forecast_desc = next(iter(response_content['weather']), {}).get('description')

    return {'temp': current_temp, 'min_temp': min_temp, 'max_temp': max_temp, 'description': forecast_desc}
