from datetime import datetime

import jwt
from flask import json
from mock import patch

from config.settings_state import Settings
from svc.manager import app


class TestGarageDoorRoutesIntegration:
    GARAGE_ID = 1
    JWT_SECRET = 'testSecret'

    def setup_method(self):
        instance = Settings.get_instance()
        instance._settings = {'JwtSecret': self.JWT_SECRET}
        flask_app = app
        self.TEST_CLIENT = flask_app.test_client()

    def test_get_garage_door_status__should_return_unauthorized_with_no_header(self):
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/status')

        assert actual.status_code == 401

    @patch('svc.controllers.garage_door_controller.get_door_duration')
    def test_get_garage_door_status__should_return_success_with_valid_jwt(self, mock_file):
        mock_file.return_value = datetime.now().isoformat()
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/status', headers=headers)

        assert actual.status_code == 200

    @patch('svc.controllers.garage_door_controller.get_door_duration')
    def test_get_garage_door_status__success_should_include_json_mime(self, mock_file):
        mock_file.return_value = datetime.now().isoformat()
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/status', headers=headers)

        assert actual.mimetype == 'application/json'

    @patch('svc.controllers.garage_door_controller.get_door_duration')
    def test_get_garage_door_status__should_include_response(self, mock_file):
        duration = datetime.now().isoformat()
        mock_file.return_value = duration
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/status', headers=headers)

        assert json.loads(actual.data) == {'isGarageOpen': True, 'statusDuration': duration,
                                           'coordinates': {'latitude': 41.621191, 'longitude': -93.831609}}

    def test_update_garage_door_state__should_return_unauthorized_without_jwt(self):
        post_body = {}
        headers = {}

        actual = self.TEST_CLIENT.post(f'garageDoor/{self.GARAGE_ID}/state', data=post_body, headers=headers)

        assert actual.status_code == 401

    def test_update_garage_door_state__should_return_success(self):
        post_body = {'garageDoorOpen': True}
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        actual = self.TEST_CLIENT.post(f'garageDoor/{self.GARAGE_ID}/state', data=json.dumps(post_body), headers=headers)

        assert actual.status_code == 200

    def test_update_garage_door_state__success_should_include_json_mime(self):
        post_body = {'garageDoorOpen': True}
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        actual = self.TEST_CLIENT.post(f'garageDoor/{self.GARAGE_ID}/state', data=json.dumps(post_body), headers=headers)

        assert actual.mimetype == 'application/json'

    def test_update_garage_door_state__should_return_bad_request_when_malformed_json(self):
        post_body = {'badKey': 'fakerequest'}
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        actual = self.TEST_CLIENT.post(f'garageDoor/{self.GARAGE_ID}/state', data=json.dumps(post_body), headers=headers)

        assert actual.status_code == 400

    def test_toggle_garage_door__should_return_success(self):
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/toggle', headers=headers)

        assert actual.status_code == 204

    def test_toggle_garage_door__should_return_unauthorized_when_invalid_jwt(self):
        bearer_token = jwt.encode({}, 'bad_secret', algorithm='HS256')
        headers = {'Authorization': bearer_token}

        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/toggle', headers=headers)

        assert actual.status_code == 401
