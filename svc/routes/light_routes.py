import json

from flask import request, Response, Blueprint

from svc.controllers.light_controller import get_assigned_lights

LIGHT_BLUEPRINT = Blueprint('light_blueprint', __name__)
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@LIGHT_BLUEPRINT.route('/lights/groups', methods=['GET'])
def get_all_assigned_lights():
    bearer_token = request.headers.get('Authorization')
    response = get_assigned_lights(bearer_token)

    return Response(json.dumps(response), status=200, headers=DEFAULT_HEADERS)
