import os

from svc.constants.lights_state import LightState
from svc.constants.settings_state import Settings
from svc.services.light_mapper import map_light_groups
from svc.utilities import api_utils
from svc.utilities.jwt_utils import is_jwt_valid


def get_assigned_light_groups(bearer_token):
    is_jwt_valid(bearer_token)
    light_state = LightState.get_instance()
    if light_state.API_KEY is None:
        settings = Settings.get_instance().get_settings()
        username = settings.get('LightApiUser') if settings.get('Development') else os.environ['LIGHT_API_USERNAME']
        password = settings.get('LightApiPass') if settings.get('Development') else os.environ['LIGHT_API_PASSWORD']
        api_key = api_utils.get_light_api_key(username, password)
    else:
        api_key = light_state.API_KEY

    light_groups = api_utils.get_light_groups(api_key)
    groups_state = __get_light_group_states(api_key, light_groups)

    return map_light_groups(light_groups, groups_state)


def set_assigned_light_groups(bearer_token, request):
    is_jwt_valid(bearer_token)
    light_state = LightState.get_instance()
    if light_state.API_KEY is None:
        settings = Settings.get_instance().get_settings()
        username = settings.get('LightApiUser') if settings.get('Development') else os.environ['LIGHT_API_USERNAME']
        password = settings.get('LightApiPass') if settings.get('Development') else os.environ['LIGHT_API_PASSWORD']
        api_key = api_utils.get_light_api_key(username, password)
    else:
        api_key = light_state.API_KEY

    api_utils.set_light_groups(api_key, request.get('groupId'), request.get('on'), request.get('brightness'))


# TODO: Investigate using GET FULL STATE api
def get_assigned_lights(bearer_token, group_id):
    is_jwt_valid(bearer_token)
    light_state = LightState.get_instance()
    if light_state.API_KEY is None:
        settings = Settings.get_instance().get_settings()
        username = settings.get('LightApiUser') if settings.get('Development') else os.environ['LIGHT_API_USERNAME']
        password = settings.get('LightApiPass') if settings.get('Development') else os.environ['LIGHT_API_PASSWORD']
        api_key = api_utils.get_light_api_key(username, password)
    else:
        api_key = light_state.API_KEY
    light_groups = api_utils.get_light_group_attributes(api_key, group_id).get('lights')
    return [__get_light_state(api_key, light) for light in light_groups]


def set_assigned_light(bearer_token, request_data):
    is_jwt_valid(bearer_token)
    light_state = LightState.get_instance()
    if light_state.API_KEY is None:
        settings = Settings.get_instance().get_settings()
        username = settings.get('LightApiUser') if settings.get('Development') else os.environ['LIGHT_API_USERNAME']
        password = settings.get('LightApiPass') if settings.get('Development') else os.environ['LIGHT_API_PASSWORD']
        api_key = api_utils.get_light_api_key(username, password)
    else:
        api_key = light_state.API_KEY

    api_utils.set_light_state(api_key, request_data.get('lightId'), request_data.get('on'), request_data.get('brightness'))


def __get_light_state(api_key, light):
    response = api_utils.get_light_state(api_key, light).get('state')
    return {light: {'on': response.get('on'), 'brightness': response.get('bri')}}


def __get_light_group_states(api_key, light_groups):
    groups_state = {k: api_utils.get_light_group_state(api_key, k) for k, v in light_groups.items()}
    return groups_state
