import base64
import json

import requests

from svc.constants.home_automation import Automation
from svc.constants.lights_state import LightState

LIGHT_BASE_URL = 'http://192.168.1.142:80/api'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'


def get_weather_by_city(city, unit, app_id):
    args = {'q': city, 'units': unit, 'APPID': app_id}
    response = requests.get(WEATHER_URL, params=args)
    return response.status_code, response.content


# TODO: may need to re-capture api key if call fails
def get_light_api_key(username, password):
    body = {'devicetype': Automation().APP_NAME}
    auth = base64.b64encode((username + ':' + password).encode('UTF-8')).decode('UTF-8')
    headers = {'Authorization': 'Basic ' + auth}
    response = requests.post(LIGHT_BASE_URL, data=json.dumps(body), headers=headers)

    return response.json()[0]['success']['username']


def get_light_groups(api_key):
    url = LIGHT_BASE_URL + '/%s/groups' % api_key
    response = requests.get(url)
    return response.json()


def set_light_groups(api_key, group_id, state, brightness=None):
    url = LIGHT_BASE_URL + '/%s/groups/%s/action' % (api_key, group_id)
    request = {'on': state}
    if brightness is not None:
        request['on'] = True
        request['bri'] = brightness

    requests.put(url, data=json.dumps(request))


def get_light_group_state(api_key, group_id):
    url = LIGHT_BASE_URL + '/%s/groups/%s' % (api_key, group_id)
    return requests.get(url).json()


def get_light_group_attributes(api_key, group_id):
    url = LIGHT_BASE_URL + '/%s/groups/%s' % (api_key, group_id)
    return requests.get(url).json()


def create_light_group(api_key, group_name):
    url = LIGHT_BASE_URL + '/%s/groups' % api_key
    request = {'name': group_name}
    requests.post(url, data=json.dumps(request))


def get_all_lights(api_key):
    url = LIGHT_BASE_URL + '/%s/lights' % api_key
    return requests.get(url).json()


def get_light_state(api_key, light_id):
    url = LIGHT_BASE_URL + '/%s/lights/%s' % (api_key, light_id)
    return requests.get(url).json()
