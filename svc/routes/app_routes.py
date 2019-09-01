from flask import Blueprint, request, Response

from svc.controllers.garage_door_controller import get_login

APP_BLUEPRINT = Blueprint('app_routes', __name__)
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@APP_BLUEPRINT.route('/healthCheck')
def health_check():
    return "Success"


# TODO: Login should return role and user id
@APP_BLUEPRINT.route('/login', methods=['GET'])
def app_login():
    bearer_token = request.headers.get('Authorization')
    jwt_token = get_login(bearer_token)
    return Response(jwt_token, status=200, headers=DEFAULT_HEADERS)
