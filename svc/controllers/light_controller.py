import os

from svc.constants.settings_state import Settings
from svc.services.light_mapper import map_light_groups
from svc.utilities.jwt_utils import is_jwt_valid


class LightController:

    def __init__(self, api_utils):
        self.API_UTILS = api_utils

    def get_assigned_lights(self, bearer_token):
        is_jwt_valid(bearer_token)
        settings = Settings.get_instance().get_settings()
        username = settings['LightApiUser'] if settings['Development'] else os.environ['LIGHT_API_USERNAME']
        password = settings['LightApiPass'] if settings['Development'] else os.environ['LIGHT_API_PASSWORD']
        api_key = self.API_UTILS.get_light_api_key(username, password)

        light_groups = self.API_UTILS.get_light_groups(api_key)
        groups_state = self.__get_light_group_states(api_key, light_groups)

        return map_light_groups(light_groups, groups_state)

    def set_assigned_lights(self, bearer_token, request):
        is_jwt_valid(bearer_token)
        settings = Settings.get_instance().get_settings()
        username = settings['LightApiUser'] if settings['Development'] else os.environ['LIGHT_API_USERNAME']
        password = settings['LightApiPass'] if settings['Development'] else os.environ['LIGHT_API_PASSWORD']
        api_key = self.API_UTILS.get_light_api_key(username, password)

        self.API_UTILS.set_light_groups(api_key, request.get('groupId'), request.get('on'), request.get('brightness'))

    def __get_light_group_states(self, api_key, light_groups):
        groups_state = {k: self.API_UTILS.get_light_group_state(api_key, k) for k, v in light_groups.items()}
        return groups_state
