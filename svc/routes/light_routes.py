import json

from flask import request, Response, Blueprint

from svc.controllers import light_controller

LIGHT_BLUEPRINT = Blueprint('light_blueprint', __name__)
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@LIGHT_BLUEPRINT.route('/lights/groups', methods=['GET'])
def get_all_assigned_lights():
    bearer_token = request.headers.get('Authorization')
    response = light_controller.get_assigned_lights(bearer_token)

    return Response(json.dumps(response), status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/lights/group/state', methods=['POST'])
def set_assigned_light_group():
    bearer_token = request.headers.get('Authorization')
    light_controller.set_assigned_lights(bearer_token, json.loads(request.data.decode('UTF-8')))

    return Response(status=200, headers=DEFAULT_HEADERS)
