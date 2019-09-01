from svc.utilities.gpio import read_temperature_file
from svc.utilities.temperature import get_user_temperature
from svc.utilities.jwt_utils import is_jwt_valid
from svc.db.methods.user_credentials import UserDatabaseManager


def get_user_temp(user_id, bearer_token):
    is_jwt_valid(bearer_token)
    with UserDatabaseManager() as database:
        database.get_preferences_by_user()
    temp_text = read_temperature_file()
    temperature = get_user_temperature(temp_text, False)

    return {'currentTemp': temperature}
