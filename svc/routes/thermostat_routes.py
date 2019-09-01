from flask import Blueprint, request

from svc.controllers.thermostat_controller import get_user_temp

THERMOSTAT_BLUEPRINT = Blueprint('thermostat_blueprint', __name__)


@THERMOSTAT_BLUEPRINT.route('/thermostat/temperature/<user_id>', methods=['GET'])
def get_temperature(user_id):
    bearer_token = request.headers.get('Authorization')
    return get_user_temp(user_id, bearer_token)
