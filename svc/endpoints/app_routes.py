from flask import Blueprint, Response

from svc.constants.home_automation import Mime


APP_BLUEPRINT = Blueprint('app_blueprint', __name__)


@APP_BLUEPRINT.route('/health', methods=['GET'])
def get_health():
    return Response('healthy', status=200, mimetype=Mime.JSON)