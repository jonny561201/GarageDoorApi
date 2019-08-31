from flask import Blueprint, request

from svc.controllers.thermostat_controller import get_user_temp

THERMOSTAT_BLUEPRINT = Blueprint('thermostat_blueprint', __name__)


@THERMOSTAT_BLUEPRINT.route('/thermostat/temperature', methods=['GET'])
def get_temperature():
    bearer_token = request.headers.get('Authorization')
    return get_user_temp(None, bearer_token)
