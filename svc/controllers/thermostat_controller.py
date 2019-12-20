import json
import os
from threading import Event

from svc.constants.hvac_state import HvacState
from svc.db.methods.user_credentials import UserDatabaseManager
from svc.services.weather_request import get_weather
from svc.utilities.event import MyThread
from svc.utilities.gpio import read_temperature_file
from svc.utilities.hvac import run_temperature_program
from svc.utilities.jwt_utils import is_jwt_valid
from svc.utilities.temperature import get_user_temperature, convert_to_celsius


ONE_MINUTE = 60


def get_user_temp(user_id, bearer_token):
    is_jwt_valid(bearer_token)
    with UserDatabaseManager() as database:
        preference = database.get_preferences_by_user(user_id)
        temp_text = read_temperature_file()
        temperature = get_user_temperature(temp_text, preference['is_fahrenheit'])
        temp_unit = "metric" if preference['temp_unit'] == "celsius" else "imperial"
        weather_data = get_weather(preference['city'], temp_unit, os.environ['WEATHER_APP_ID'])

        response = {'currentTemp': temperature, 'isFahrenheit': preference['is_fahrenheit']}
        response.update(weather_data)

        return response


def set_user_temperature(request, bearer_token):
    is_jwt_valid(bearer_token)
    json_request = json.loads(request.decode('UTF-8'))
    temp = convert_to_celsius(json_request['desiredTemp']) if json_request['isFahrenheit'] else json_request['desiredTemp']
    state = HvacState.get_instance()
    __create_hvac_thread(state)
    state.MODE = json_request['mode']
    state.DESIRED_TEMP = temp


def __create_hvac_thread(state):
    if state.ACTIVE_THREAD is None:
        stop_event = Event()
        state.STOP_EVENT = stop_event
        state.ACTIVE_THREAD = MyThread(stop_event, run_temperature_program, ONE_MINUTE)
        state.ACTIVE_THREAD.start()
