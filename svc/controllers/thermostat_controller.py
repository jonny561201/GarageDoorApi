import json
import os
from threading import Event

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.services.weather_request import get_weather
from svc.utilities.event import MyThread
from svc.utilities.gpio import read_temperature_file
from svc.utilities.hvac import Hvac
from svc.utilities.jwt_utils import is_jwt_valid
from svc.utilities.temperature import get_user_temperature, convert_to_celsius


def get_user_temp(user_id, bearer_token):
    is_jwt_valid(bearer_token)
    with UserDatabaseManager() as database:
        preference = database.get_preferences_by_user(user_id)
        temp_text = read_temperature_file()
        temperature = get_user_temperature(temp_text, preference['is_fahrenheit'])
        weather_data = get_weather(preference['city'], preference['temp_unit'], os.environ['WEATHER_APP_ID'])

        response = {'currentTemp': temperature, 'isFahrenheit': preference['is_fahrenheit']}
        response.update(weather_data)

        return response


class SetThermostat:
    ONE_MINUTE = 60
    STOP_FLAG = None
    ACTIVE_THREAD = None

    def set_user_temperature(self, request, bearer_token):
        is_jwt_valid(bearer_token)
        json_request = json.loads(request.decode('UTF-8'))
        if self.ACTIVE_THREAD is not None:
            self.STOP_FLAG.set()
        temp = convert_to_celsius(json_request['desiredTemp']) if json_request['isFahrenheit'] else json_request['desiredTemp']
        hvac_utility = Hvac(temp, json_request['mode'])
        self.STOP_FLAG = Event()
        self.ACTIVE_THREAD = MyThread(self.STOP_FLAG, hvac_utility.run_temperature_program, self.ONE_MINUTE)
        self.ACTIVE_THREAD.start()
