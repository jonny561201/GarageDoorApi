from flask import Response, Blueprint
from flask import json
from flask import request

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.jwt_utils import create_jwt_token, is_jwt_valid

route_blueprint = Blueprint('route_blueprint', __name__)
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@route_blueprint.route('/healthcheck')
def health_check():
    return "Success"


@route_blueprint.route('/garageDoor/login', methods=['POST'])
def garage_door_login():
    post_body = request.data
    with UserDatabaseManager() as user_database:
        if user_database.user_credentials_are_valid(post_body):
            jwt_token = create_jwt_token()
            return Response(jwt_token, status=200)
        else:
            return Response(status=401)


@route_blueprint.route('/garageDoor/status', methods=['GET'])
def garage_door_status():
    if not is_jwt_valid(request.headers.get('Authorization')):
        return Response(status=401)
    body = json.dumps({'garageStatus': True})
    return Response(body, status=200, headers=DEFAULT_HEADERS)


@route_blueprint.route('/garageDoor/state', methods=['POST'])
def update_garage_door_state():
    if not is_jwt_valid(request.headers.get('Authorization')):
        return Response(status=401)
    request_body = request.data
    return Response(json.dumps(request_body), status=200, headers=DEFAULT_HEADERS)
