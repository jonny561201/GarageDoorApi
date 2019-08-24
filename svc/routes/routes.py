from flask import Response, Blueprint
from flask import json
from flask import request

from svc.controllers.garage_door_controller import get_login, get_status, update_state

route_blueprint = Blueprint('route_blueprint', __name__)
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@route_blueprint.route('/healthCheck')
def health_check():
    return "Success"


@route_blueprint.route('/garageDoor/login', methods=['POST'])
def garage_door_login():
    bearer_token = request.headers.get('Authorization')
    jwt_token = get_login(bearer_token)
    return Response(jwt_token, status=200, headers=DEFAULT_HEADERS)


@route_blueprint.route('/garageDoor/status', methods=['GET'])
def get_garage_door_status():
    bearer_token = request.headers.get('Authorization')
    status = get_status(bearer_token)
    return Response(status, status=200, headers=DEFAULT_HEADERS)


@route_blueprint.route('/garageDoor/state', methods=['POST'])
def update_garage_door_state():
    bearer_token = request.headers.get('Authorization')
    updated_state = update_state(bearer_token, request.data)
    return Response(json.dumps(updated_state), status=200, headers=DEFAULT_HEADERS)
