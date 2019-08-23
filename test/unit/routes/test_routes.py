import os
from datetime import datetime, timedelta

import jwt
import pytz
from flask import json
from mock import patch

from svc.routes.routes import get_garage_door_status, update_garage_door_state, garage_door_login


@patch('svc.routes.routes.request')
class TestAppRoutes:
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    @patch('svc.routes.routes.garage_door_status')
    def test_garage_door_status__should_call_get_garage_door_status(self, mock_gpio, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_gpio.return_value = {}
        get_garage_door_status()

        mock_gpio.assert_called()

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

    def test_garage_door_status__should_return_unauthorized_if_provided_bad_jwt(self, mock_request):
        jwt_token = jwt.encode({'user_id': 12345}, 'bad_secret', algorithm='HS256').decode('UTF-8')
        mock_request.headers = {'Authorization': jwt_token}

        actual = get_garage_door_status()

        assert actual.status_code == 401

    def test_garage_door_status__should_return_unauthorized_if_provided_no_header(self, mock_request):
        mock_request.headers = {}

        actual = get_garage_door_status()

        assert actual.status_code == 401

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

    @patch('svc.routes.routes.UserDatabaseManager')
    def test_garage_door_login__should_respond_with_success_status_code(self, mock_credentials, mock_request):
        mock_request.data = '{}'
        mock_credentials.return_value.__enter__.return_value.are_credentials_valid.return_value = True

        actual = garage_door_login()

        assert actual.status_code == 200

    @patch('svc.utilities.jwt_utils.datetime')
    @patch('svc.routes.routes.UserDatabaseManager')
    def test_garage_door_login__should_respond_with_jwt_token(self, mock_credentials, mock_datetime, mock_request):
        mock_request.data = '{}'
        now = datetime.now(tz=pytz.timezone('US/Central'))
        mock_datetime.now.return_value = now
        mock_credentials.return_value.__enter__.return_value.are_credentials_valid.return_value = True
        expected_expire = now + timedelta(hours=2)
        truncated_date = (str(expected_expire.timestamp() * 1000))[:10]
        expected_token = {'user_id': 12345, 'exp': int(truncated_date)}

        actual = garage_door_login()

        assert jwt.decode(actual.data, self.JWT_SECRET, algorithms=["HS256"]) == expected_token

    @patch('svc.routes.routes.UserDatabaseManager')
    def test_garage_door_login__should_respond_with_unauthorized_status_code_when_user_not_valid(self, mock_credentials, mock_request):
        mock_request.data = '{}'
        mock_credentials.return_value.__enter__.return_value.are_credentials_valid.return_value = False

        actual = garage_door_login()

        assert actual.status_code == 401

    @patch('svc.routes.routes.UserDatabaseManager')
    def test_garage_door_login__should_call_validate_credentials_with_post_body(self, mock_credentials, mock_request):
        post_body = '{"username": "fakeUser", "password": "fakePass"}'
        mock_request.data = post_body
        garage_door_login()

        mock_credentials.return_value.__enter__.return_value.are_credentials_valid.assert_called_with(json.loads(post_body))
