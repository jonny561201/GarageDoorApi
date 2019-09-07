from svc.controllers.sump_controller import get_sump_level


def get_current_sump_level(user_id):
    depth = get_sump_level(user_id)
    return depth