import base64
import os

import jwt
import pytest
from flask import json
from mock import patch
from werkzeug.exceptions import Unauthorized

from svc.routes.routes import get_garage_door_status, update_garage_door_state, garage_door_login


@patch('svc.routes.routes.request')
class TestAppRoutes:
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')
    USER = 'user_name'
    PWORD = 'password'
    CREDS = ('%s:%s' % (USER, PWORD)).encode()
    ENCODED_CREDS = base64.b64encode(CREDS).decode('UTF-8')
    AUTH_HEADER = {"Authorization": "Basic " + ENCODED_CREDS}

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    @patch('svc.routes.routes.get_status')
    def test_garage_door_status__should_call_get_status(self, mock_controller, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}

        get_garage_door_status()

        mock_controller.assert_called_with(self.JWT_TOKEN)

    def test_garage_door_status__should_return_success_status_code(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        actual = get_garage_door_status()

        assert actual.status_code == 200

    def test_garage_door_status__should_return_success_header(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        expected_headers = 'text/json'

        actual = get_garage_door_status()

        assert actual.content_type == expected_headers

    def test_garage_door_status__should_return_response_body(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        expected_body = {"isGarageOpen": True}

        actual = get_garage_door_status()
        json_actual = json.loads(actual.data)

        assert json_actual == expected_body

    def test_garage_door_status__should_raises_when_unauthorized(self, mock_request):
        mock_request.headers = {}

        with pytest.raises(Unauthorized):
            get_garage_door_status()

    def test_update_garage_door_state__should_return_success_status_code(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_request.data = '{}'.encode()
        actual = update_garage_door_state()

        assert actual.status_code == 200

    def test_update_garage_door_state__should_return_success_header(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_request.data = '{}'.encode()
        expected_headers = 'text/json'

        actual = update_garage_door_state()

        assert actual.content_type == expected_headers

    def test_update_garage_door_state__should_check_state_with_request(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        post_body = '{"testBody": "testValues"}'
        mock_request.data = post_body.encode()

        actual = update_garage_door_state()
        json_actual = json.loads(actual.data)

        assert json_actual == post_body

    def test_update_garage_door_state__should_return_unauthorized_if_provided_bad_jwt(self, mock_request):
        jwt_token = jwt.encode({'user_id': 12345}, 'bad_secret', algorithm='HS256').decode('UTF-8')
        mock_request.headers = {'Authorization': jwt_token}
        mock_request.data = {}

        actual = update_garage_door_state()

        assert actual.status_code == 401

    @patch('svc.routes.routes.update_garage_door')
    def test_update_garage_door_state__should_call_update_gpio(self, mock_gpio, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        request = {"Test": "abc"}
        mock_request.data = json.dumps(request).encode()
        update_garage_door_state()

        mock_gpio.assert_called_with(request)

    @patch('svc.routes.routes.get_login')
    def test_garage_door_login__should_respond_with_success_status_code(self, mock_login, mock_request):
        mock_request.headers = self.AUTH_HEADER

        actual = garage_door_login()

        assert actual.status_code == 200

    @patch('svc.routes.routes.get_login')
    def test_garage_door_login__should_respond_with_success_login_response(self, mock_login, mock_request):
        jwt_token = 'fakeJwtToken'
        mock_request.headers = self.AUTH_HEADER
        mock_login.return_value = jwt_token

        actual = garage_door_login()

        assert actual.data == jwt_token.encode()

    @patch('svc.routes.routes.get_login')
    def test_garage_door_login__should_call_get_login(self, mock_login, mock_request):
        mock_request.headers = self.AUTH_HEADER
        garage_door_login()

        expected_bearer = "Basic " + self.ENCODED_CREDS
        mock_login.assert_called_with(expected_bearer)
