from flask import json
from mock import patch, MagicMock
from werkzeug.exceptions import Unauthorized

from svc.manager import create_app


class TestAppRoutesIntegration:
    FAKE_API_KEY = 'FAKE_API_KEY'

    def setup_method(self):
        self.APP = create_app()
        self.APP.mdns = MagicMock()
        self.TEST_CLIENT = self.APP.test_client()

    def test_get_health__should_return_success(self):
        actual = self.TEST_CLIENT.get('/health')

        assert actual.status_code == 200

    @patch('svc.endpoints.app_routes.app_controller.confirm_registration')
    def test_confirm_registration__should_return_success(self, mock_confirm):
        mock_confirm.return_value = self.FAKE_API_KEY

        actual = self.TEST_CLIENT.post('/register')

        assert actual.status_code == 200

    @patch('svc.endpoints.app_routes.app_controller.confirm_registration')
    def test_confirm_registration__should_pass_body_and_mdns_to_controller(self, mock_confirm):
        mock_confirm.return_value = self.FAKE_API_KEY

        self.TEST_CLIENT.post('/register', json={'api_key': self.FAKE_API_KEY})

        mock_confirm.assert_called_once_with({'api_key': self.FAKE_API_KEY}, self.APP.mdns)

    @patch('svc.endpoints.app_routes.app_controller.confirm_registration')
    def test_confirm_registration__should_pass_none_body_when_no_json(self, mock_confirm):
        mock_confirm.return_value = self.FAKE_API_KEY

        self.TEST_CLIENT.post('/register')

        mock_confirm.assert_called_once_with(None, self.APP.mdns)

    @patch('svc.endpoints.app_routes.app_controller.confirm_registration')
    def test_confirm_registration__should_return_api_key_in_json_response(self, mock_confirm):
        mock_confirm.return_value = self.FAKE_API_KEY

        actual = self.TEST_CLIENT.post('/register')

        result = json.loads(actual.data)
        assert result['api_key'] == self.FAKE_API_KEY

    @patch('svc.endpoints.app_routes.app_controller.confirm_registration')
    def test_confirm_registration__should_return_unauthorized_when_controller_raises(self, mock_confirm):
        mock_confirm.side_effect = Unauthorized()

        actual = self.TEST_CLIENT.post('/register', json={'api_key': 'wrong_key'})

        assert actual.status_code == 401

