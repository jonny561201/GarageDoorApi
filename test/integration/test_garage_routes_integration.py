from datetime import datetime

import jwt
from flask import json
from mock import patch

from integration.integration_helper import mock_jwks_token
from svc.config.settings_state import Settings
from svc.manager import app


@patch('svc.controllers.garage_door_controller.file_utils')
class TestGarageDoorRoutesIntegration:
    GARAGE_ID = 1

    def setup_method(self):
        token = mock_jwks_token()
        self.HEADERS = {'Authorization': token}
        flask_app = app
        self.TEST_CLIENT = flask_app.test_client()

    def test_get_garage_door_status__should_return_unauthorized_with_no_header(self, mock_file):
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/status')

        assert actual.status_code == 401

    def test_get_garage_door_status__should_return_success_with_valid_jwt(self, mock_file):
        mock_file.get_door_duration.return_value = datetime.now()
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/status', headers=self.HEADERS)

        assert actual.status_code == 200

    def test_get_garage_door_status__success_should_include_json_mime(self, mock_file):
        mock_file.get_door_duration.return_value = datetime.now()
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/status', headers=self.HEADERS)

        assert actual.mimetype == 'application/json'

    def test_get_garage_door_status__should_include_response(self, mock_file):
        duration = datetime.now()
        mock_file.get_door_duration.return_value = duration
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/status', headers=self.HEADERS)

        assert json.loads(actual.data) == {'garageId': str(self.GARAGE_ID), 'isGarageOpen': True, 'statusDuration': duration.isoformat(),
                                           'coordinates': {'latitude': 41.621191, 'longitude': -93.831609}}

    def test_update_garage_door_state__should_return_unauthorized_without_jwt(self, mock_file):
        post_body = {}
        headers = {}

        actual = self.TEST_CLIENT.post(f'garageDoor/{self.GARAGE_ID}/state', data=post_body, headers=headers)

        assert actual.status_code == 401

    def test_update_garage_door_state__should_return_success(self, mock_file):
        post_body = {'open': True}

        actual = self.TEST_CLIENT.post(f'garageDoor/{self.GARAGE_ID}/state', data=json.dumps(post_body), headers=self.HEADERS)

        assert actual.status_code == 200

    def test_update_garage_door_state__success_should_include_json_mime(self, mock_file):
        post_body = {'open': True}

        actual = self.TEST_CLIENT.post(f'garageDoor/{self.GARAGE_ID}/state', data=json.dumps(post_body), headers=self.HEADERS)

        assert actual.mimetype == 'application/json'

    def test_update_garage_door_state__should_return_bad_request_when_malformed_json(self, mock_file):
        post_body = {'badKey': 'fakerequest'}

        actual = self.TEST_CLIENT.post(f'garageDoor/{self.GARAGE_ID}/state', data=json.dumps(post_body), headers=self.HEADERS)

        assert actual.status_code == 400

    def test_toggle_garage_door__should_return_success(self, mock_file):
        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/toggle', headers=self.HEADERS)

        assert actual.status_code == 204

    def test_toggle_garage_door__should_return_unauthorized_when_invalid_jwt(self, mock_file):
        bearer_token = jwt.encode({}, 'bad_secret', algorithm='HS256')
        headers = {'Authorization': bearer_token}

        actual = self.TEST_CLIENT.get(f'garageDoor/{self.GARAGE_ID}/toggle', headers=headers)

        assert actual.status_code == 401

    def test_get_all_statuses__should_return_unauthorized_with_no_header(self, mock_file):
        actual = self.TEST_CLIENT.get('garageDoor/status')

        assert actual.status_code == 401

    def test_get_all_statuses__should_return_success_with_valid_jwt(self, mock_file):
        mock_file.get_door_duration.return_value = datetime.now()

        actual = self.TEST_CLIENT.get('garageDoor/status', headers=self.HEADERS)

        assert actual.status_code == 200

    def test_get_all_statuses__should_return_json_mime(self, mock_file):
        mock_file.get_door_duration.return_value = datetime.now()

        actual = self.TEST_CLIENT.get('garageDoor/status', headers=self.HEADERS)

        assert actual.mimetype == 'application/json'

    def test_get_all_statuses__should_return_list_of_two_statuses(self, mock_file):
        duration = datetime.now()
        mock_file.get_door_duration.return_value = duration

        actual = self.TEST_CLIENT.get('garageDoor/status', headers=self.HEADERS)

        result = json.loads(actual.data)
        assert result['coordinates'] == {'latitude': 41.621191, 'longitude': -93.831609}
        assert len(result['doors']) == 2
        assert result['doors'][0]['garageId'] == '1'
        assert result['doors'][1]['garageId'] == '2'

