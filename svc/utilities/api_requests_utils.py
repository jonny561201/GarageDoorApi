import base64
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
    auth = base64.b64encode((username + ':' + password).encode('UTF-8')).decode('UTF-8')
    headers = {'Authorization': 'Basic ' + auth}
    response = requests.post(url, data=json.dumps(body), headers=headers)

    return response.json()[0]['success']['username']
