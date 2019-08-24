from werkzeug.exceptions import Unauthorized

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.credentials import extract_credentials
from svc.utilities.jwt_utils import create_jwt_token


def get_login(bearer_token):
    user, pword = extract_credentials(bearer_token)
    with UserDatabaseManager() as user_database:
        if user_database.are_credentials_valid(user, pword):
            return create_jwt_token()
        else:
            raise Unauthorized
