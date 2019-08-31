from flask import Blueprint

from svc.controllers.thermostat_controller import get_user_temp

THERMOSTAT_BLUEPRINT = Blueprint('thermostat_blueprint', __name__)


@THERMOSTAT_BLUEPRINT.route('/thermostat/temperature', methods=['GET'])
def get_temperature():
    get_user_temp(None, None)
    return '32.15'
