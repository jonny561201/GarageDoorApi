import json

from flask import Blueprint, request, Response

from svc.controllers.sump_controller import get_sump_level

SUMP_BLUEPRINT = Blueprint('sump_pump_blueprint', __name__)
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@SUMP_BLUEPRINT.route('/sumpPump/user/<user_id>/depth', methods=['GET'])
def get_current_sump_level(user_id):
    bearer_token = request.headers.get('Authorization')
    depth = get_sump_level(user_id, bearer_token)
    return Response(json.dumps(depth), status=200, headers=DEFAULT_HEADERS)
