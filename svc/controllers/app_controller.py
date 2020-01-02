import json

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.jwt_utils import create_jwt_token, is_jwt_valid, extract_credentials


def get_login(basic_token):
    user_name, pword = extract_credentials(basic_token)
    with UserDatabaseManager() as user_database:
        user_id = user_database.validate_credentials(user_name, pword)
        return create_jwt_token(user_id)


def get_user_preferences(bearer_token, user_id):
    is_jwt_valid(bearer_token)
    with UserDatabaseManager() as database:
        return database.get_preferences_by_user(user_id)


def save_user_preferences(bearer_token, user_id, request_data):
    is_jwt_valid(bearer_token)
    user_preferences = json.loads(request_data.decode('UTF-8'))
    with UserDatabaseManager() as database:
        database.insert_preferences_by_user(user_id, user_preferences)
