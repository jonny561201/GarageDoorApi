from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.credentials import extract_credentials
from svc.utilities.jwt_utils import create_jwt_token, is_jwt_valid


def get_login(basic_token):
    user_name, pword = extract_credentials(basic_token)
    with UserDatabaseManager() as user_database:
        user_id = user_database.validate_credentials(user_name, pword)
        return create_jwt_token(user_id)


def get_user_preferences(bearer_token, user_id):
    is_jwt_valid(bearer_token)
