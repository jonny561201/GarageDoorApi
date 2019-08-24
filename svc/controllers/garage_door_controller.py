import json

from werkzeug.exceptions import Unauthorized

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.credentials import extract_credentials
from svc.utilities.gpio import garage_door_status
from svc.utilities.jwt_utils import create_jwt_token, is_jwt_valid


def get_login(bearer_token):
    user, pword = extract_credentials(bearer_token)
    with UserDatabaseManager() as user_database:
        if user_database.are_credentials_valid(user, pword):
            return create_jwt_token()
        else:
            raise Unauthorized


def get_status(bearer_token):
    if not is_jwt_valid(bearer_token):
        raise Unauthorized
    return json.dumps(garage_door_status())
