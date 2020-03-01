import os

from mock import patch, ANY

from svc.controllers.light_controller import get_assigned_light_groups, set_assigned_light_groups, get_assigned_lights, \
    set_assigned_light


@patch('svc.controllers.light_controller.LightState')
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

    def test_get_assigned_light_groups__should_call_is_jwt_valid(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = None
        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)

    def test_get_assigned_light_groups__should_call_to_get_api_key(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = None
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': False}
        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_api.get_light_api_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)

    def test_get_assigned_light_groups__should_use_settings_light_user_name_pass_when_dev(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = None
        light_user = 'otherLightUser'
        light_pass = 'otherLightPass'
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': True, 'LightApiUser': light_user,
                                                                        'LightApiPass': light_pass}

        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_api.get_light_api_key.assert_called_with(light_user, light_pass)

    # def test_get_assigned_light_groups__should_pass_api_key_to_get_light_groups(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
    #     mock_light.get_instance.return_value.API_KEY = None
    #     mock_api.get_light_api_key.return_value = self.API_KEY
    #     get_assigned_light_groups(self.BEARER_TOKEN)
    #
    #     mock_api.get_light_groups.assert_called_with(self.API_KEY)

    # def test_get_assigned_light_groups__should_map_response_from_light_group_api(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
    #     api_response = {'field': 'my value doesnt matter'}
    #     mock_api.get_light_groups.return_value = api_response
    #
    #     get_assigned_light_groups(self.BEARER_TOKEN)
    #
    #     mock_map.assert_called_with(api_response, ANY)
    #
    # def test_get_assigned_light_groups__should_map_response_from_group_state_api(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
    #     group_one_state = {'action': {'on': False}}
    #     group_two_state = {'action': {'on': True}}
    #     mock_api.get_light_groups.return_value = {'1': {}, '3': {}}
    #     mock_api.get_light_group_state.side_effect = [group_one_state, group_two_state]
    #     expected_groups = {'1': group_one_state, '3': group_two_state}
    #
    #     get_assigned_light_groups(self.BEARER_TOKEN)
    #
    #     assert mock_api.get_light_group_state.call_count == 2
    #     mock_map.assert_called_with(ANY, expected_groups)
    #
    # def test_get_assigned_light_groups__should_return_response_from_mapper(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
    #     map_response = {'other_field': 'also doesnt matter'}
    #     mock_map.return_value = map_response
    #
    #     actual = get_assigned_light_groups(self.BEARER_TOKEN)
    #
    #     assert actual == map_response
    #
    # def test_get_assigned_light_groups__should_call_to_get_light_group_state(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
    #     mock_light.get_instance.return_value.API_KEY = None
    #     light_groups = {'1': {}}
    #     mock_api.get_light_api_key.return_value = self.API_KEY
    #     mock_api.get_light_groups.return_value = light_groups
    #     get_assigned_light_groups(self.BEARER_TOKEN)
    #
    #     mock_api.get_light_group_state.assert_called_with(self.API_KEY, '1')

    def test_get_assigned_light_groups__should_use_cached_api_key(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        new_api_key = 'NewApiKey'
        mock_light.get_instance.return_value.API_KEY = new_api_key
        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_api.get_light_api_key.assert_not_called()
        mock_api.get_full_state.assert_called_with(new_api_key)

    def test_set_assigned_light_groups__should_call_is_jwt_valid(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)

    def test_set_assigned_light_groups__should_get_api_key(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = None
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': False}
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_api.get_light_api_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)

    def test_set_assigned_light_groups__should_get_lights_with_settings_if_develop(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = None
        light_user = 'otherLightUser'
        light_pass = 'otherLightPass'
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': True, 'LightApiUser': light_user,
                                                                        'LightApiPass': light_pass}
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_api.get_light_api_key.assert_called_with(light_user, light_pass)

    def test_set_assigned_light_groups__should_make_api_call_to_set_state(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = None
        api_key = 'fakeApiKey'
        mock_api.get_light_api_key.return_value = api_key
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_api.set_light_groups.assert_called_with(api_key, self.GROUP_ID, self.STATE, None)

    def test_set_assigned_light_groups__should_make_api_call_to_set_brightness_optionally(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        brightness = 255
        self.REQUEST['brightness'] = brightness
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_api.set_light_groups.assert_called_with(ANY, ANY, ANY, brightness)

    def test_set_assigned_light_groups__should_use_cached_api_key(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        new_api_key = 'NewApiKey'
        mock_light.get_instance.return_value.API_KEY = new_api_key
        set_assigned_light_groups(self.BEARER_TOKEN, self.REQUEST)

        mock_api.get_light_api_key.assert_not_called()
        mock_set.get_instance.assert_not_called()
        mock_api.set_light_groups.assert_called_with(new_api_key, ANY, ANY, ANY)

    def test_get_assigned_lights__should_call_is_jwt_valid(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        get_assigned_lights(self.BEARER_TOKEN, self.GROUP_ID)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)

    def test_get_assigned_lights__should_make_call_to_get_api_key(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': False}
        mock_light.get_instance.return_value.API_KEY = None
        get_assigned_lights(self.BEARER_TOKEN, self.GROUP_ID)

        mock_api.get_light_api_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)

    def test_get_assigned_lights__should_use_settings_user_pass_when_in_dev_mode(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        light_user = 'LightUser'
        light_pass = 'LightPass'
        mock_light.get_instance.return_value.API_KEY = None
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': True, 'LightApiUser': light_user,
                                                                        'LightApiPass': light_pass}
        get_assigned_lights(self.BEARER_TOKEN, self.GROUP_ID)

        mock_api.get_light_api_key.assert_called_with(light_user, light_pass)

    def test_get_assigned_lights__should_call_to_get_group_attributes(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = None
        mock_api.get_light_api_key.return_value = self.API_KEY
        get_assigned_lights(self.BEARER_TOKEN, self.GROUP_ID)

        mock_api.get_light_group_attributes.assert_called_with(self.API_KEY, self.GROUP_ID)

    def test_get_assigned_lights__should_use_cached_api_key(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        api_key = 'fakeApiKey'
        mock_light.get_instance.return_value.API_KEY = api_key
        get_assigned_lights(self.BEARER_TOKEN, self.GROUP_ID)

        mock_api.get_light_api_key.assert_not_called()
        mock_set.get_instance.assert_not_called()
        mock_api.get_light_group_attributes.assert_called_with(api_key, self.GROUP_ID)

    def test_get_assigned_lights__should_call_get_lights_for_each_light(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        api_key = 'fakeApiKey'
        mock_api.get_light_group_attributes.return_value = {'lights': ['1', '2']}
        mock_light.get_instance.return_value.API_KEY = api_key
        get_assigned_lights(self.BEARER_TOKEN, self.GROUP_ID)

        assert mock_api.get_light_state.call_count == 2
        mock_api.get_light_state.assert_any_call(api_key, '1')
        mock_api.get_light_state.assert_any_call(api_key, '2')

    def test_get_assigned_lights__should_return_the_lights_brightness_and_status(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        api_key = 'fakeApiKey'
        mock_api.get_light_group_attributes.return_value = {'lights': ['1', '2']}
        mock_light.get_instance.return_value.API_KEY = api_key
        light_one = {'state': {'bri': 144, 'on': False}}
        light_two = {'state': {'bri': 255, 'on': True}}
        mock_api.get_light_state.side_effect = [light_one, light_two]

        actual = get_assigned_lights(self.BEARER_TOKEN, self.GROUP_ID)

        assert actual == [{'1': {'on': False, 'brightness': 144}}, {'2': {'on': True, 'brightness': 255}}]

    def test_set_assigned_light__should_call_is_jwt_valid(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        request_data = {'lightId': '4', 'on': True, 'brightness': 179}
        set_assigned_light(self.BEARER_TOKEN, request_data)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)

    def test_set_assigned_light__should_make_api_call_to_get_key(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        request_data = {'lightId': '3', 'on': False, 'brightness': 201}
        mock_light.get_instance.return_value.API_KEY = None
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': False}
        set_assigned_light(self.BEARER_TOKEN, request_data)

        mock_api.get_light_api_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)

    def test_set_assigned_light__should_use_dev_key_when_in_dev_mode(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        request_data = {'lightId': '5', 'on': True, 'brightness': 45}
        light_user = 'newUser'
        light_pass = 'newPass'
        mock_light.get_instance.return_value.API_KEY = None
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': True, 'LightApiUser': light_user,
                                                                        'LightApiPass': light_pass}
        set_assigned_light(self.BEARER_TOKEN, request_data)

        mock_api.get_light_api_key.assert_called_with(light_user, light_pass)

    def test_set_assigned_light__should_make_call_to_set_light_state(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        light_id = '2'
        brightness = 65
        request_data = {'lightId': light_id, 'on': True, 'brightness': brightness}
        mock_light.get_instance.return_value.API_KEY = None
        mock_set.get_instance.return_value.get_settings.return_value = {'Development': False}
        mock_api.get_light_api_key.return_value = self.API_KEY
        set_assigned_light(self.BEARER_TOKEN, request_data)

        mock_api.set_light_state.assert_called_with(self.API_KEY, light_id, True, brightness)

    def test_set_assigned_light__should_use_cached_api_key_when_on_state(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        light_id = '1'
        brightness = 176
        request_data = {'lightId': light_id, 'on': False, 'brightness': brightness}
        new_key = 'fakeNewApiKey'
        mock_light.get_instance.return_value.API_KEY = new_key
        set_assigned_light(self.BEARER_TOKEN, request_data)

        mock_api.get_light_api_key.assert_not_called()
        mock_set.get_instance.assert_not_called()
        mock_api.set_light_state.assert_called_with(new_key, light_id, False, brightness)

    def test_get_assigned_light_groups__should_make_api_call_to_get_full_state(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = self.API_KEY
        get_assigned_light_groups(self.BEARER_TOKEN)

        mock_api.get_full_state.assert_called_with(self.API_KEY)

    def test_get_assigned_light_groups__should_return_mapped_response(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = self.API_KEY
        brightness = 233
        group_name = 'LivingRoom'
        mock_api.get_full_state.return_value = {
            'groups': {'1': {'action': {'on': True, 'bri': brightness}, 'name': group_name}}, 'lights': {}}
        actual = get_assigned_light_groups(self.BEARER_TOKEN)

        assert actual == [{'groupId': '1', 'groupName': group_name, 'on': True, 'brightness': brightness, 'lights': []}]

    def test_get_assigned_light_groups__should_map_the_lights_in_a_group(self, mock_api, mock_map, mock_jwt, mock_set, mock_light):
        mock_light.get_instance.return_value.API_KEY = self.API_KEY
        light_1 = {'name': 'lamp 1', 'state': {'on': True, 'bri': 233}}
        light_2 = {'name': 'lamp 2', 'state': {'on': False, 'bri': 0}}
        light_3 = {'name': 'lamp 3', 'state': {'on': False, 'bri': 255}}
        lights = {'1': light_1, '2': light_2, '3': light_3}
        mock_api.get_full_state.return_value = {'groups': {'2': {'action': {}, 'lights': ['1', '3']}}, 'lights': lights}

        actual = get_assigned_light_groups(self.BEARER_TOKEN)

        assert actual == [{'groupId': '2', 'groupName': None, 'brightness': None, 'on': None,
                           'lights': [{'lightId': '1', 'lightName': 'lamp 1', 'on': True, 'brightness': 233},
                                      {'lightId': '3', 'lightName': 'lamp 3', 'on': False, 'brightness': 255}]}]
