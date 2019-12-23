import json
import logging

from requests.exceptions import ConnectionError
from werkzeug.exceptions import Unauthorized

from svc.utilities.api_requests import get_weather_by_city


def get_weather(city, unit, app_id):
    status_code = None
    json_response = {}
    try:
        status_code, content = get_weather_by_city(city, unit, app_id)
        json_response = json.loads(content)
    except ConnectionError:
        logging.info('Weather API connection error!')

    __validate_response(status_code)
    return __build_response(json_response)


def __validate_response(status_code):
    if status_code == 401:
        raise Unauthorized


def __build_response(response_content):
    main = response_content.get('main', {})
    current_temp = main.get('temp', 0.0)
    min_temp = main.get('temp_min', 0.0)
    max_temp = main.get('temp_max', 0.0)
    forecast_desc = next(iter(response_content.get('weather', {})), {}).get('description')

    return {'temp': current_temp, 'minTemp': min_temp, 'maxTemp': max_temp, 'description': forecast_desc}
