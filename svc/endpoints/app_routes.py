import json

from flask import Blueprint, Response, current_app

from svc.constants.home_automation import Mime
from svc.utilities.api_key_utils import get_generate_api_key

APP_BLUEPRINT = Blueprint('app_blueprint', __name__)


@APP_BLUEPRINT.route('/health', methods=['GET'])
def get_health():
    return Response('healthy', status=200, mimetype=Mime.JSON)


@APP_BLUEPRINT.route('/register', methods=['POST'])
def confirm_registration():
    api_key = get_generate_api_key()
    current_app.mdns.unregister()
    return Response(json.dumps({'api_key': api_key}), status=200, mimetype=Mime.JSON)
