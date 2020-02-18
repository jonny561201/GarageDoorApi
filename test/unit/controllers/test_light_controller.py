import os

from mock import patch, ANY

from svc.controllers.light_controller import get_assigned_lights, set_assigned_lights


@patch('svc.controllers.light_controller.is_jwt_valid')
@patch('svc.controllers.light_controller.map_light_groups')
@patch('svc.controllers.light_controller.api_utils')
class TestLightRequest:
    LIGHT_USERNAME = "fakeUsername"
    LIGHT_PASSWORD = "fakePassword"
    API_KEY = "fakeApiKey"
    BEARER_TOKEN = "EAK#K$%B$#K#"

    def setup_method(self):
        os.environ.update({'LIGHT_API_USERNAME': self.LIGHT_USERNAME})
        os.environ.update({'LIGHT_API_PASSWORD': self.LIGHT_PASSWORD})

    def teardown_method(self):
        os.environ.pop('LIGHT_API_USERNAME')
        os.environ.pop('LIGHT_API_PASSWORD')

    def test_get_assigned_lights__should_call_is_jwt_valid(self, mock_api, mock_map, mock_jwt):
        get_assigned_lights(self.BEARER_TOKEN)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)

    def test_get_assigned_lights__should_call_to_get_api_key(self, mock_api, mock_map, mock_jwt):
        get_assigned_lights(self.BEARER_TOKEN)

        mock_api.get_light_api_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)

    def test_get_assigned_lights__should_pass_api_key_to_get_light_groups(self, mock_api, mock_map, mock_jwt):
        mock_api.get_light_api_key.return_value = self.API_KEY
        get_assigned_lights(self.BEARER_TOKEN)

        mock_api.get_light_groups.assert_called_with(self.API_KEY)

    def test_get_assigned_lights__should_map_response_from_light_group_api(self, mock_api, mock_map, mock_jwt):
        api_response = {'field': 'my value doesnt matter'}
        mock_api.get_light_groups.return_value = api_response

        get_assigned_lights(self.BEARER_TOKEN)

        mock_map.assert_called_with(api_response, ANY)

    def test_get_assigned_lights__should_map_response_from_group_state_api(self, mock_api, mock_map, mock_jwt):
        group_one_state = {'action': {'on': False}}
        group_two_state = {'action': {'on': True}}
        mock_api.get_light_groups.return_value = {'1': {}, '3': {}}
        mock_api.get_light_group_state.side_effect = [group_one_state, group_two_state]
        expected_groups = {'1': group_one_state, '3': group_two_state}

        get_assigned_lights(self.BEARER_TOKEN)

        assert mock_api.get_light_group_state.call_count == 2
        mock_map.assert_called_with(ANY, expected_groups)

    def test_get_assigned_lights__should_return_response_from_mapper(self, mock_api, mock_map, mock_jwt):
        map_response = {'other_field': 'also doesnt matter'}
        mock_map.return_value = map_response

        actual = get_assigned_lights(self.BEARER_TOKEN)

        assert actual == map_response

    def test_get_assigned_lights__should_call_to_get_light_group_state(self, mock_api, mock_map, mock_jwt):
        light_groups = {'1': {}}
        mock_api.get_light_api_key.return_value = self.API_KEY
        mock_api.get_light_groups.return_value = light_groups
        get_assigned_lights(self.BEARER_TOKEN)

        mock_api.get_light_group_state.assert_called_with(self.API_KEY, '1')

    def test_set_assigned_lights__should_call_is_jwt_valid(self, mock_api, mock_map, mock_jwt):
        set_assigned_lights(self.BEARER_TOKEN)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)


