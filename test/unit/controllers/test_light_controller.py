import os

from mock import patch, ANY

from svc.controllers.light_controller import get_assigned_light_groups, set_assigned_light_groups


@patch('svc.controllers.light_controller.Settings')
@patch('svc.controllers.light_controller.is_jwt_valid')
@patch('svc.controllers.light_controller.map_light_groups')
@patch('svc.controllers.light_controller.api_utils')
class TestLightRequest:
    LIGHT_USERNAME = "fakeUsername"
    LIGHT_PASSWORD = "fakePassword"
    API_KEY = "fakeApiKey"
    BEARER_TOKEN = "EAK#K$%B$#K#"
    GROUP_ID = '1'
    STATE = False

    def setup_method(self):
        self.REQUEST = {'on': self.STATE, 'groupId': self.GROUP_ID}
        os.environ.update({'LIGHT_API_USERNAME': self.LIGHT_USERNAME})
        os.environ.update({'LIGHT_API_PASSWORD': self.LIGHT_PASSWORD})

    def teardown_method(self):
        os.environ.pop('LIGHT_API_USERNAME')
        os.environ.pop('LIGHT_API_PASSWORD')

    def test_get_assigned_light_groups__should_call_is_jwt_valid(self, mock_api, mock_map, mock_jwt, mock_set):
        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)

    def test_get_assigned_light_groups__should_call_to_get_api_key(self, mock_api, mock_map, mock_jwt, mock_set):
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': False}
        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_api.get_light_api_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)

    def test_get_assigned_light_groups__should_use_settings_light_user_name_pass_when_dev(self, mock_api, mock_map, mock_jwt, mock_set):
        light_user = 'otherLightUser'
        light_pass = 'otherLightPass'
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': True, 'LightApiUser': light_user,
                                                                        'LightApiPass': light_pass}

        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_api.get_light_api_key.assert_called_with(light_user, light_pass)

    def test_get_assigned_light_groups__should_pass_api_key_to_get_light_groups(self, mock_api, mock_map, mock_jwt, mock_set):
        mock_api.get_light_api_key.return_value = self.API_KEY
        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_api.get_light_groups.assert_called_with(self.API_KEY)

    def test_get_assigned_light_groups__should_map_response_from_light_group_api(self, mock_api, mock_map, mock_jwt, mock_set):
        api_response = {'field': 'my value doesnt matter'}
        mock_api.get_light_groups.return_value = api_response

        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_map.assert_called_with(api_response, ANY)

    def test_get_assigned_light_groups__should_map_response_from_group_state_api(self, mock_api, mock_map, mock_jwt, mock_set):
        group_one_state = {'action': {'on': False}}
        group_two_state = {'action': {'on': True}}
        mock_api.get_light_groups.return_value = {'1': {}, '3': {}}
        mock_api.get_light_group_state.side_effect = [group_one_state, group_two_state]
        expected_groups = {'1': group_one_state, '3': group_two_state}

        get_assigned_light_groups(self.BEARER_TOKEN)

        assert mock_api.get_light_group_state.call_count == 2
        mock_map.assert_called_with(ANY, expected_groups)

    def test_get_assigned_light_groups__should_return_response_from_mapper(self, mock_api, mock_map, mock_jwt, mock_set):
        map_response = {'other_field': 'also doesnt matter'}
        mock_map.return_value = map_response

        actual = get_assigned_light_groups(self.BEARER_TOKEN)

        assert actual == map_response

    def test_get_assigned_light_groups__should_call_to_get_light_group_state(self, mock_api, mock_map, mock_jwt, mock_set):
        light_groups = {'1': {}}
        mock_api.get_light_api_key.return_value = self.API_KEY
        mock_api.get_light_groups.return_value = light_groups
        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_api.get_light_group_state.assert_called_with(self.API_KEY, '1')

    def test_set_assigned_light_groups__should_call_is_jwt_valid(self, mock_api, mock_map, mock_jwt, mock_set):
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)

    def test_set_assigned_light_groups__should_get_api_key(self, mock_api, mock_map, mock_jwt, mock_set):
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': False}
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_api.get_light_api_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)

    def test_set_assigned_light_groups__should_get_lights_with_settings_if_develop(self, mock_api, mock_map, mock_jwt, mock_set):
        light_user = 'otherLightUser'
        light_pass = 'otherLightPass'
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': True, 'LightApiUser': light_user,
                                                                        'LightApiPass': light_pass}
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_api.get_light_api_key.assert_called_with(light_user, light_pass)

    def test_set_assigned_light_groups__should_make_api_call_to_set_state(self, mock_api, mock_map, mock_jwt, mock_set):
        api_key = 'fakeApiKey'
        mock_api.get_light_api_key.return_value = api_key
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_api.set_light_groups.assert_called_with(api_key, self.GROUP_ID, self.STATE, None)

    def test_set_assigned_light_groups__should_make_api_call_to_set_brightness_optionally(self, mock_api, mock_map, mock_jwt, mock_set):
        brightness = 255
        self.REQUEST['brightness'] = brightness
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_api.set_light_groups.assert_called_with(ANY, ANY, ANY, brightness)

    # def test_get_assigned_lights__should_call_is_jwt_valid(self, mock_api, mock_map, mock_jwt, mock_set):
    # get_assigned_l
