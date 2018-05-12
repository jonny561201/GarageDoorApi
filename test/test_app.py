import os

import jwt
from flask import json
from mock import patch

from app import garage_door_status, update_garage_door_state, garage_door_login


class TestAppRoutes():
    JWT_SECRET = 'fake_jwt_secret'

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    def test_garage_door_status__should_return_success_status_code(self):
        actual = garage_door_status()

        assert actual.status_code == 200

    def test_garage_door_status__should_return_success_header(self):
        expected_headers = 'text/json'

        actual = garage_door_status()

        assert actual.content_type == expected_headers

    def test_garage_door_status__should_return_response_body(self):
        expected_body = '{"garageStatus": true}'

        actual = garage_door_status()

        assert actual.data == expected_body

    @patch('app.request')
    def test_update_garage_door_state__should_return_success_status_code(self, mock_request):
        mock_request.data = {}
        actual = update_garage_door_state()

        assert actual.status_code == 200

    @patch('app.request')
    def test_update_garage_door_state__should_return_success_header(self, mock_request):
        mock_request.data = {}
        expected_headers = 'text/json'

        actual = update_garage_door_state()

        assert actual.content_type == expected_headers

    @patch('app.request')
    def test_update_garage_door_state__should_check_state_with_request(self, mock_request):
        post_body = {"testBody": "testValues"}
        mock_request.data = post_body

        actual = update_garage_door_state()

        assert actual.data == '{}'.format(json.dumps(post_body))

    @patch('app.user_credentials_are_valid')
    def test_garage_door_login__should_respond_with_success_status_code(self, mock_credentials):
        mock_credentials.return_value = True
        actual = garage_door_login()

        assert actual.status_code == 200

    @patch('app.user_credentials_are_valid')
    def test_garage_door_login__should_respond_with_jwt_token(self, mock_credentials):
        mock_credentials.return_value = True
        expected_token = {'user_id': 12345}
        actual = garage_door_login()

        assert jwt.decode(actual.data, self.JWT_SECRET, algorithms=["HS256"]) == expected_token

    @patch('app.user_credentials_are_valid')
    def test_garage_door_login__should_respond_with_unauthorized_when_user_not_valid(self, mock_credentials):
        mock_credentials.return_value = False
        actual = garage_door_login()

        assert actual.status_code == 401
