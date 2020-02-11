import json

import requests

from svc.constants.home_automation import Automation


def get_weather_by_city(city, unit, app_id):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    args = {'q': city, 'units': unit, 'APPID': app_id}

    response = requests.get(base_url, params=args)

    return response.status_code, response.content


def get_light_api_key(username, password):
    url = 'http://192.168.1.139:8080/api'
    body = {'devicetype': Automation().APP_NAME}
    requests.post(url, data=json.dumps(body))
