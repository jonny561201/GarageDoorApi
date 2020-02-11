import os

from mock import patch

from svc.services.light_request import get_assigned_lights


@patch('svc.services.light_request.get_light_api_key')
class TestLightRequest:
    LIGHT_USERNAME = "fakeUsername"
    LIGHT_PASSWORD = "fakePassword"

    def setup_method(self):
        os.environ.update({'LIGHT_API_USERNAME': self.LIGHT_USERNAME})
        os.environ.update({'LIGHT_API_PASSWORD': self.LIGHT_PASSWORD})

    def teardown_method(self):
        os.environ.pop('LIGHT_API_USERNAME')
        os.environ.pop('LIGHT_API_PASSWORD')

    def test_get_assigned_lights__should_call_to_get_api_key(self, mock_get_key):
        get_assigned_lights()

        mock_get_key.assert_called_with(self.LIGHT_USERNAME, self.LIGHT_PASSWORD)
