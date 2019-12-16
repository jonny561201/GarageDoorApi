from flask import Blueprint, request

from svc.controllers.thermostat_controller import get_user_temp
from svc.controllers.thermostat_controller import SetThermostat

THERMOSTAT_BLUEPRINT = Blueprint('thermostat_blueprint', __name__)


@THERMOSTAT_BLUEPRINT.route('/thermostat/temperature/<user_id>', methods=['GET'])
def get_temperature(user_id):
    bearer_token = request.headers.get('Authorization')
    return get_user_temp(user_id, bearer_token)


def set_temperature(user_id):
    bearer_token = request.headers.get('Authorization')
    # TODO: should start up in app
    SetThermostat().set_user_temperature(request.data, bearer_token)

