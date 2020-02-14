import os

from svc.utilities import api_requests_utils
from svc.services.light_mapper import map_light_groups


def get_assigned_lights():
    username = os.environ['LIGHT_API_USERNAME']
    password = os.environ['LIGHT_API_PASSWORD']
    api_key = api_requests_utils.get_light_api_key(username, password)

    light_groups = api_requests_utils.get_light_groups(api_key)
    groups_state = {}
    for k, v in light_groups.items():
        group_state = api_requests_utils.get_light_group_state(api_key, k)
        groups_state[k] = group_state

    return map_light_groups(light_groups, groups_state)
