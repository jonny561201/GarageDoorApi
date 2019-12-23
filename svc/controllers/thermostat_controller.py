import json
from threading import Event

from svc.constants.home_automation import Automation
from svc.constants.hvac_state import HvacState
from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.event import MyThread
from svc.utilities.hvac import run_temperature_program
from svc.utilities.jwt_utils import is_jwt_valid
from svc.utilities.temperature import convert_to_celsius
from svc.services import temperature_service


def get_user_temp(user_id, bearer_token):
    is_jwt_valid(bearer_token)
    with UserDatabaseManager() as database:
        preference = database.get_preferences_by_user(user_id)
        internal_temp = temperature_service.get_internal_temp(preference)
        weather_data = temperature_service.get_external_temp(preference)

        return __create_response(internal_temp, preference['is_fahrenheit'], weather_data)


# TODO: mode should also support being off!
def set_user_temperature(request, bearer_token):
    is_jwt_valid(bearer_token)
    json_request = json.loads(request.decode('UTF-8'))
    temp = convert_to_celsius(json_request['desiredTemp']) if json_request['isFahrenheit'] else json_request['desiredTemp']
    state = HvacState.get_instance()
    __create_hvac_thread(state)
    state.MODE = json_request['mode']
    state.DESIRED_TEMP = temp


def __create_response(internal_temp, is_fahren, weather_data):
    state = HvacState.get_instance()
    response = {'currentTemp': internal_temp, 'isFahrenheit': is_fahren,
                'minThermostatTemp': 50.0 if is_fahren else 10.0,
                'maxThermostatTemp': 90.0 if is_fahren else 32.0,
                'mode': state.MODE, 'desiredTemp': state.DESIRED_TEMP}
    response.update(weather_data)
    return response


def __create_hvac_thread(state):
    if state.ACTIVE_THREAD is None:
        stop_event = Event()
        state.STOP_EVENT = stop_event
        state.ACTIVE_THREAD = MyThread(stop_event, run_temperature_program, Automation.TIME.ONE_MINUTE)
        state.ACTIVE_THREAD.start()
