import json

from flask import request, Response

from svc.controllers.light_controller import get_assigned_lights


DEFAULT_HEADERS = {'Content-Type': 'text/json'}


def get_all_assigned_lights():
    bearer_token = request.headers.get('Authorization')
    response = get_assigned_lights(bearer_token)

    return Response(json.dumps(response), status=200, headers=DEFAULT_HEADERS)
