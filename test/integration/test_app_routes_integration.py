from flask import json
from mock import patch, MagicMock

from svc.manager import create_app


class TestAppRoutesIntegration:
    FAKE_API_KEY = 'FAKE_API_KEY'

    def setup_method(self):
        self.APP = create_app()
        self.TEST_CLIENT = self.APP.test_client()

    def test_get_health__should_return_success(self):
        actual = self.TEST_CLIENT.get('/health')

        assert actual.status_code == 200

    @patch('svc.endpoints.app_routes.get_generate_api_key')
    def test_confirm_registration__should_return_success(self, mock_generate):
        mock_generate.return_value = self.FAKE_API_KEY
        self.APP.mdns = MagicMock()

        actual = self.TEST_CLIENT.post('/register')

        assert actual.status_code == 200

    @patch('svc.endpoints.app_routes.get_generate_api_key')
    def test_confirm_registration__should_call_unregister(self, mock_generate):
        mock_generate.return_value = self.FAKE_API_KEY
        self.APP.mdns = MagicMock()

        self.TEST_CLIENT.post('/register')

        self.APP.mdns.unregister.assert_called_once()

    @patch('svc.endpoints.app_routes.get_generate_api_key')
    def test_confirm_registration__should_return_api_key_in_json_response(self, mock_generate):
        mock_generate.return_value = self.FAKE_API_KEY
        self.APP.mdns = MagicMock()

        actual = self.TEST_CLIENT.post('/register')

        result = json.loads(actual.data)
        assert result['api_key'] == self.FAKE_API_KEY

