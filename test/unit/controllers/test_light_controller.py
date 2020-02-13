import os

from mock import patch

from svc.controllers.light_controller import get_assigned_lights


@patch('svc.controllers.light_controller.map_light_groups')
@patch('svc.controllers.light_controller.api_requests_utils')
class TestLightRequest:
    LIGHT_USERNAME = "fakeUsername"
    LIGHT_PASSWORD = "fakePassword"
    API_KEY = "fakeApiKey"

    def setup_method(self):
        os.environ.update({'LIGHT_API_USERNAME': self.LIGHT_USERNAME})
        os.environ.update({'LIGHT_API_PASSWORD': self.LIGHT_PASSWORD})

    def teardown_method(self):
        os.environ.pop('LIGHT_API_USERNAME')
        os.environ.pop('LIGHT_API_PASSWORD')

    def test_get_assigned_lights__should_call_to_get_api_key(self, mock_api, mock_map):
        get_assigned_lights()

        mock_api.get_light_api_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)

    def test_get_assigned_lights__should_pass_api_key_to_get_light_groups(self, mock_api, mock_map):
        mock_api.get_light_api_key.return_value = self.API_KEY
        get_assigned_lights()

        mock_api.get_light_groups.assert_called_with(self.API_KEY)

    def test_get_assigned_lights__should_map_response_from_api(self, mock_api, mock_map):
        api_response = {'field': 'my value doesnt matter'}
        mock_api.get_light_groups.return_value = api_response

        get_assigned_lights()

        mock_map.assert_called_with(api_response)

    def test_get_assigned_lights__should_return_response_from_mapper(self, mock_api, mock_map):
        map_response = {'other_field': 'also doesnt matter'}
        mock_map.return_value = map_response

        actual = get_assigned_lights()

        assert actual == map_response