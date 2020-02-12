import os

from svc.utilities.api_requests_utils import get_light_api_key
from svc.utilities.api_requests_utils import get_light_groups


def get_assigned_lights():
    username = os.environ['LIGHT_API_USERNAME']
    password = os.environ['LIGHT_API_PASSWORD']
    api_key = get_light_api_key(username, password)

    get_light_groups(api_key)
