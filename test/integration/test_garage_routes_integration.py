import os

import jwt
from flask import json
from mock import patch

from svc.manager import app


class TestGarageDoorRoutesIntegration:
    GARAGE_ID = 1
    TEST_CLIENT = None
    JWT_SECRET = 'testSecret'

    def setup_method(self):
        flask_app = app
        self.TEST_CLIENT = flask_app.test_client()
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self):
        os.environ.pop('JWT_SECRET')

    def test_get_garage_door_status__should_return_unauthorized_with_no_header(self):
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/status')

        assert actual.status_code == 401

    @patch('svc.utilities.file_utils.get_door_duration')
    def test_get_garage_door_status__should_return_success_with_valid_jwt(self, mock_file):
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}
        url = f'garageDoor/{self.GARAGE_ID}/status'
        actual = self.TEST_CLIENT.get(url, headers=headers)

        assert actual.status_code == 200

    def test_update_garage_door_state__should_return_unauthorized_without_jwt(self):
        post_body = {}
        headers = {}

        url = f'garageDoor/{self.GARAGE_ID}/state'
        actual = self.TEST_CLIENT.post(url, data=post_body, headers=headers)

        assert actual.status_code == 401

    def test_update_garage_door_state__should_return_success(self):
        post_body = {'garageDoorOpen': True}
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        url = f'garageDoor/{self.GARAGE_ID}/state'
        actual = self.TEST_CLIENT.post(url, data=json.dumps(post_body), headers=headers)

        assert actual.status_code == 200

    def test_update_garage_door_state__should_return_bad_request_when_malformed_json(self):
        post_body = {'badKey': 'fakerequest'}
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        url = f'garageDoor/{self.GARAGE_ID}/state'
        actual = self.TEST_CLIENT.post(url, data=json.dumps(post_body), headers=headers)

        assert actual.status_code == 400

    def test_toggle_garage_door__should_return_success(self):
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        url = f'garageDoor/{self.GARAGE_ID}/toggle'
        actual = self.TEST_CLIENT.get(url, headers=headers)

        assert actual.status_code == 200

    def test_toggle_garage_door__should_return_unauthorized_when_invalid_jwt(self):
        bearer_token = jwt.encode({}, 'bad_secret', algorithm='HS256')
        headers = {'Authorization': bearer_token}

        url = f'garageDoor/{self.GARAGE_ID}/toggle'
        actual = self.TEST_CLIENT.get(url, headers=headers)

        assert actual.status_code == 401
