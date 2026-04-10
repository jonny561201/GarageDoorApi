from flask import Response, Blueprint
from flask import request

from svc.constants.home_automation import Mime
from svc.controllers import garage_door_controller


GARAGE_BLUEPRINT = Blueprint('garage_blueprint', __name__, url_prefix='/garageDoor')


@GARAGE_BLUEPRINT.route('/status', methods=['GET'])
def get_all_garage_door_statuses():
    api_key = request.headers.get('X-API-Key')
    statuses = garage_door_controller.get_all_statuses(api_key)
    return Response(statuses.to_json(), status=200, mimetype=Mime.JSON)


@GARAGE_BLUEPRINT.route('/<garage_id>/status', methods=['GET'])
def get_garage_door_status(garage_id):
    api_key = request.headers.get('X-API-Key')
    status = garage_door_controller.get_status(api_key, garage_id)
    return Response(status.to_json(), status=200, mimetype=Mime.JSON)


@GARAGE_BLUEPRINT.route('/<garage_id>/state', methods=['POST'])
def update_garage_door_state(garage_id):
    api_key = request.headers.get('X-API-Key')
    updated_state = garage_door_controller.update_door_state(api_key, garage_id, request.data)
    return Response(updated_state.to_json(), status=200, mimetype=Mime.JSON)


@GARAGE_BLUEPRINT.route('/<garage_id>/toggle', methods=['GET'])
def toggle_garage_door(garage_id):
    api_key = request.headers.get('X-API-Key')
    garage_door_controller.toggle_door(api_key, garage_id)
    return Response(status=204)
