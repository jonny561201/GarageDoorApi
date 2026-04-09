from flask import Blueprint, Response, current_app

from svc.constants.home_automation import Mime


APP_BLUEPRINT = Blueprint('app_blueprint', __name__)


@APP_BLUEPRINT.route('/health', methods=['GET'])
def get_health():
    return Response('healthy', status=200, mimetype=Mime.JSON)


@APP_BLUEPRINT.route('/register', methods=['POST'])
def confirm_registration():
    current_app.mdns.unregister()
    return Response(status=200)
