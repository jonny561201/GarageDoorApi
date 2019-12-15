from svc.db.methods.user_credentials import UserDatabaseManager
from svc.services.weather_request import get_weather
from svc.utilities.gpio import read_temperature_file
from svc.utilities.jwt_utils import is_jwt_valid
from svc.utilities.temperature import get_user_temperature
from svc.utilities.hvac import Hvac
from svc.utilities.event import MyThread


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

    def set_user_temperature(self, request, bearer_token):
        is_jwt_valid(bearer_token)
        mode = request['mode']
        desired_temp = request['desiredTemp']
        hvac_utility = Hvac(desired_temp, mode)
        hvac_thread = MyThread(self.STOP_FLAG, hvac_utility.run_temperature_program, self.ONE_MINUTE)
        hvac_thread.start()
        # need controller that stores only one active event
        # controller will always stop event and start new one when api call is made
