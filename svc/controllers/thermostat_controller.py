import os

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.gpio import read_temperature_file
from svc.utilities.jwt_utils import is_jwt_valid
from svc.utilities.temperature import get_user_temperature
from svc.utilities.api_requests import get_weather_by_city


def get_user_temp(user_id, bearer_token):
    is_jwt_valid(bearer_token)
    with UserDatabaseManager() as database:
        #TODO: preferences needs to store city name, temperature unit
        preference = database.get_preferences_by_user(user_id)
        temp_text = read_temperature_file()
        temperature = get_user_temperature(temp_text, preference['is_fahrenheit'])
        weather_data = get_weather_by_city('London', 'imperial', os.environ['WEATHER_APP_ID'])

        response = {'currentTemp': temperature, 'isFahrenheit': preference['is_fahrenheit']}
        response.update(weather_data)

        return response
