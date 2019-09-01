import json

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.credentials import extract_credentials
from svc.utilities.gpio import garage_door_status, update_garage_door
from svc.utilities.jwt_utils import create_jwt_token, is_jwt_valid


def get_login(bearer_token):
    user, pword = extract_credentials(bearer_token)
    with UserDatabaseManager() as user_database:
        user_database.are_credentials_valid(user, pword)
    return create_jwt_token()


def get_status(bearer_token):
    is_jwt_valid(bearer_token)
    status = garage_door_status()
    return {'isGarageOpen': status}


def update_state(bearer_token, request):
    is_jwt_valid(bearer_token)
    request_body = request.decode('UTF-8')
    new_state = update_garage_door(json.loads(request_body))
    return {'garageDoorOpen': new_state}
