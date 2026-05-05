import json

from flask import Blueprint, Response, current_app, request

from svc.constants.home_automation import Mime
from svc.controllers import app_controller


APP_BLUEPRINT = Blueprint('app_blueprint', __name__)


@APP_BLUEPRINT.route('/health', methods=['GET'])
def get_health():
    return Response('healthy', status=200, mimetype=Mime.JSON)


@APP_BLUEPRINT.route('/register', methods=['POST'])
def confirm_registration():
    body = request.get_json(silent=True)
    api_key = app_controller.confirm_registration(body, current_app.mdns)
    return Response(json.dumps({'api_key': api_key}), status=200, mimetype=Mime.JSON)
