import os

from mock import patch

from svc.controllers.light_controller import get_assigned_lights


@patch('svc.controllers.light_controller.get_light_groups')
@patch('svc.controllers.light_controller.get_light_api_key')
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

    def test_get_assigned_lights__should_call_to_get_api_key(self, mock_key, mock_get):
        get_assigned_lights()

        mock_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)

    def test_get_assigned_lights__should_pass_api_key_to_get_light_groups(self, mock_key, mock_get):
        mock_key.return_value = self.API_KEY
        get_assigned_lights()

        mock_get.assert_called_with(self.API_KEY)
