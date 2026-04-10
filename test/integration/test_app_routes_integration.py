from flask import json
from mock import patch, MagicMock

from svc.manager import app


class TestAppRoutesIntegration:
    FAKE_API_KEY = 'FAKE_API_KEY'

    def setup_method(self):
        self.TEST_CLIENT = app.test_client()

    def test_get_health__should_return_success(self):
        actual = self.TEST_CLIENT.get('/health')

        assert actual.status_code == 200

    @patch('svc.endpoints.app_routes.get_generate_api_key')
    def test_confirm_registration__should_return_success(self, mock_generate):
        mock_generate.return_value = self.FAKE_API_KEY
        app.mdns = MagicMock()

        actual = self.TEST_CLIENT.post('/register')

        assert actual.status_code == 200

    @patch('svc.endpoints.app_routes.get_generate_api_key')
    def test_confirm_registration__should_call_unregister(self, mock_generate):
        mock_generate.return_value = self.FAKE_API_KEY
        app.mdns = MagicMock()

        self.TEST_CLIENT.post('/register')

        app.mdns.unregister.assert_called_once()

    @patch('svc.endpoints.app_routes.get_generate_api_key')
    def test_confirm_registration__should_return_api_key_in_json_response(self, mock_generate):
        mock_generate.return_value = self.FAKE_API_KEY
        app.mdns = MagicMock()

        actual = self.TEST_CLIENT.post('/register')

        result = json.loads(actual.data)
        assert result['api_key'] == self.FAKE_API_KEY

