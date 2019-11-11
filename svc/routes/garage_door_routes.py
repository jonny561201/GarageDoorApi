from flask import Response, Blueprint
from flask import json
from flask import request

from svc.controllers.garage_door_controller import get_status, update_state, toggle_garage_door_state

GARAGE_BLUEPRINT = Blueprint('garage_blueprint', __name__)
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@GARAGE_BLUEPRINT.route('/garageDoor/status', methods=['GET'])
def get_garage_door_status():
    bearer_token = request.headers.get('Authorization')
    status = get_status(bearer_token)
    return Response(json.dumps(status), status=200, headers=DEFAULT_HEADERS)


@GARAGE_BLUEPRINT.route('/garageDoor/state', methods=['POST'])
def update_garage_door_state():
    bearer_token = request.headers.get('Authorization')
    updated_state = update_state(bearer_token, request.data)
    return Response(json.dumps(updated_state), status=200, headers=DEFAULT_HEADERS)


# TODO: add endpoint to toggle state
def toggle_garage_door():
    bearer_token = request.headers.get('Authorization')
    toggle_garage_door_state(bearer_token)