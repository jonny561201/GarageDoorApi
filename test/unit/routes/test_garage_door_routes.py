import os
from datetime import datetime

import jwt
from flask import json
from mock import patch

from svc.routes.garage_door_routes import get_garage_door_status, update_garage_door_state, toggle_garage_door


@patch('svc.routes.garage_door_routes.garage_door_controller')
@patch('svc.routes.garage_door_routes.request')
class TestAppRoutes:
    GARAGE_ID = 1
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    def test_garage_door_status__should_call_get_status(self, mock_request, mock_controller):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_controller.get_status.return_value = {}

        get_garage_door_status(self.GARAGE_ID)

        mock_controller.get_status.assert_called_with(self.JWT_TOKEN)

    def test_garage_door_status__should_return_success_status_code(self, mock_request, mock_controller):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_controller.get_status.return_value = {}
        actual = get_garage_door_status(self.GARAGE_ID)

        assert actual.status_code == 200

    def test_garage_door_status__should_return_success_header(self, mock_request, mock_controller):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_controller.get_status.return_value = {}
        expected_headers = 'text/json'

        actual = get_garage_door_status(self.GARAGE_ID)

        assert actual.content_type == expected_headers

    def test_garage_door_status__should_return_response_body(self, mock_request, mock_controller):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        expected_body = {"isGarageOpen": True, "statusDuration": datetime.now()}
        mock_controller.get_status.return_value = expected_body

        actual = get_garage_door_status(self.GARAGE_ID)

        assert actual.data.decode('UTF-8') == json.dumps(expected_body)

    def test_update_garage_door_state__should_return_success_status_code(self, mock_request, mock_controller):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_request.data = '{"garageDoorOpen": "False"}'.encode()
        mock_controller.update_state.return_value = {}
        actual = update_garage_door_state(self.GARAGE_ID)

        assert actual.status_code == 200

    def test_update_garage_door_state__should_return_success_header(self, mock_request, mock_controller):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_request.data = '{"garageDoorOpen": "True"}'.encode()
        mock_controller.update_state.return_value = {}
        expected_headers = 'text/json'

        actual = update_garage_door_state(self.GARAGE_ID)

        assert actual.content_type == expected_headers

    def test_update_garage_door_state__should_check_state_with_request(self, mock_request, mock_controller):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        post_body = '{"garageDoorOpen": "True"}'
        mock_request.data = post_body.encode()
        expected_response = {'fakeResponse': True}
        mock_controller.update_state.return_value = expected_response

        actual = update_garage_door_state(self.GARAGE_ID)
        json_actual = json.loads(actual.data)

        assert json_actual == expected_response

    def test_toggle_garage_door__should_call_controller_with_bearer_token(self, mock_request, mock_controller):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        toggle_garage_door()

        mock_controller.toggle_door.assert_called_with(self.JWT_TOKEN)

    def test_toggle_garage_door__should_return_success_status_code(self, mock_request, mock_controller):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        actual = toggle_garage_door()

        assert actual.status_code == 200

    def test_toggle_garage_door__should_return_success_headers(self, mock_request, mock_controller):
        expected_headers = 'text/json'
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        actual = toggle_garage_door()

        assert actual.content_type == expected_headers
