from flask import Blueprint

from svc.controllers.sump_controller import get_sump_level

SUMP_BLUEPRINT = Blueprint('sump_pump_blueprint', __name__)


@SUMP_BLUEPRINT.route('/sumpPump/user/<user_id>/depth', methods=['GET'])
def get_current_sump_level(user_id):
    depth = get_sump_level(user_id)
    return depth
