from flask import Blueprint

THERMOSTAT_BLUEPRINT = Blueprint('thermostat_blueprint', __name__)


@THERMOSTAT_BLUEPRINT.route('/thermostat/temperature', methods=['GET'])
def get_temperature():
    return '32.15'
