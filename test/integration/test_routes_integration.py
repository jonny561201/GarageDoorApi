import base64
import os

import jwt
from flask import json

from svc.manager import create_app


class TestRouteIntegration:
    test_client = None
    JWT_SECRET = 'testSecret'

    def setup_method(self):
        flask_app = create_app('__main__')
        self.test_client = flask_app.test_client()
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self):
        os.environ.pop('JWT_SECRET')

    def test_health_check__should_return_success(self):
        actual = self.test_client.get('healthCheck')

        assert actual.status_code == 200
        assert actual.data.decode('UTF-8') == 'Success'

    def test_get_garage_door_status__should_return_unauthorized(self):
        actual = self.test_client.get('garageDoor/status')

        assert actual.status_code == 401

    def test_get_garage_door_status__should_return_success_with_valid_jwt(self):
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}
        actual = self.test_client.get('garageDoor/status', headers=headers)

        assert actual.status_code == 200

    def test_update_garage_door_state__should_return_unauthorized_without_jwt(self):
        post_body = {}
        headers = {}

        actual = self.test_client.post('garageDoor/state', data=post_body, headers=headers)

        assert actual.status_code == 401

    def test_update_garage_door_state__should_return_success(self):
        post_body = {'garageDoorOpen': True}
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        actual = self.test_client.post('garageDoor/state', data=json.dumps(post_body), headers=headers)

        assert actual.status_code == 200

    def test_update_garage_door_state__should_return_bad_request_when_malformed_json(self):
        post_body = {'badKey': 'fakerequest'}
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        actual = self.test_client.post('garageDoor/state', data=json.dumps(post_body), headers=headers)

        assert actual.status_code == 400

    def test_garage_door_login__should_return_401_when_invalid_user(self):
        user_name = 'not_real_user'
        user_pass = 'wrongPass'
        creds = "%s:%s" % (user_name, user_pass)
        headers = {'Authorization': base64.b64encode(creds.encode())}

        actual = self.test_client.get('garageDoor/login', headers=headers)

        assert actual.status_code == 401

    def test_garage_door_login__should_return_401_when_invalid_password(self):
        user_name = 'Jonny561201'
        user_pass = 'wrongPass'
        creds = "%s:%s" % (user_name, user_pass)
        headers = {'Authorization': base64.b64encode(creds.encode())}

        actual = self.test_client.get('garageDoor/login', headers=headers)

        assert actual.status_code == 401

    def test_garage_door_login__should_return_200_when_user_valid(self):
        user_name = 'Jonny561201'
        user_pass = 'password'
        creds = "%s:%s" % (user_name, user_pass)
        headers = {'Authorization': base64.b64encode(creds.encode())}

        actual = self.test_client.get('garageDoor/login', headers=headers)

        assert actual.status_code == 200
