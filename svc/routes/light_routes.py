import json

from flask import request, Response, Blueprint

from svc.controllers import light_controller

LIGHT_BLUEPRINT = Blueprint('light_blueprint', __name__)
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@LIGHT_BLUEPRINT.route('/lights/groups', methods=['GET'])
def get_assigned_light_groups():
    bearer_token = request.headers.get('Authorization')
    response = light_controller.get_assigned_light_groups(bearer_token)

    return Response(json.dumps(response), status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/lights/group/state', methods=['POST'])
def set_assigned_light_group():
    bearer_token = request.headers.get('Authorization')
    light_controller.set_assigned_light_groups(bearer_token, json.loads(request.data.decode('UTF-8')))

    return Response(status=200, headers=DEFAULT_HEADERS)


def get_lights_assigned_to_group(group_id):
    bearer_token = request.headers.get('Authorization')
    light_controller.get_assigned_lights(bearer_token, group_id)
    return Response(status=200)
