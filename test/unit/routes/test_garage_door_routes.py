import os
from datetime import datetime

import jwt
import pytest
from flask import json
from mock import patch
from werkzeug.exceptions import Unauthorized, BadRequest

from svc.routes.garage_door_routes import get_garage_door_status, update_garage_door_state, toggle_garage_door


@patch('svc.routes.garage_door_routes.request')
class TestAppRoutes:
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    @patch('svc.routes.garage_door_routes.get_status')
    def test_garage_door_status__should_call_get_status(self, mock_controller, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_controller.return_value = {}

        get_garage_door_status()

        mock_controller.assert_called_with(self.JWT_TOKEN)

    @patch('svc.routes.garage_door_routes.get_status')
    def test_garage_door_status__should_return_success_status_code(self, mock_status, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_status.return_value = {}
        actual = get_garage_door_status()

        assert actual.status_code == 200

    @patch('svc.routes.garage_door_routes.get_status')
    def test_garage_door_status__should_return_success_header(self, mock_status, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_status.return_value = {}
        expected_headers = 'text/json'

        actual = get_garage_door_status()

        assert actual.content_type == expected_headers

    @patch('svc.routes.garage_door_routes.get_status')
    def test_garage_door_status__should_return_response_body(self, mock_status, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        expected_body = {"isGarageOpen": True, "statusDuration": datetime.now()}
        mock_status.return_value = expected_body

        actual = get_garage_door_status()

        assert actual.data.decode('UTF-8') == json.dumps(expected_body)

    def test_garage_door_status__should_raises_when_unauthorized(self, mock_request):
        mock_request.headers = {}

        with pytest.raises(Unauthorized):
            get_garage_door_status()

    def test_update_garage_door_state__should_return_success_status_code(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_request.data = '{"garageDoorOpen": "False"}'.encode()
        actual = update_garage_door_state()

        assert actual.status_code == 200

    def test_update_garage_door_state__should_return_success_header(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        mock_request.data = '{"garageDoorOpen": "True"}'.encode()
        expected_headers = 'text/json'

        actual = update_garage_door_state()

        assert actual.content_type == expected_headers

    @patch('svc.routes.garage_door_routes.update_state')
    def test_update_garage_door_state__should_check_state_with_request(self, mock_state, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        post_body = '{"garageDoorOpen": "True"}'
        mock_request.data = post_body.encode()
        expected_response = {'fakeResponse': True}
        mock_state.return_value = expected_response

        actual = update_garage_door_state()
        json_actual = json.loads(actual.data)

        assert json_actual == expected_response

    def test_update_garage_door_state__should_raise_unauthorized_if_provided_bad_jwt(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        post_body = '{"testBody": "testValues"}'
        mock_request.data = post_body.encode()

        with pytest.raises(BadRequest):
            update_garage_door_state()

    def test_update_garage_door_state__should_raise_bad_request_when_provided_bad_json(self, mock_request):
        jwt_token = jwt.encode({'user_id': 12345}, 'bad_secret', algorithm='HS256').decode('UTF-8')
        mock_request.headers = {'Authorization': jwt_token}
        mock_request.data = {}

        with pytest.raises(Unauthorized):
            update_garage_door_state()

    @patch('svc.routes.garage_door_routes.toggle_garage_door_state')
    def test_toggle_garage_door__should_call_controller_with_bearer_token(self, mock_controller, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        toggle_garage_door()

        mock_controller.assert_called_with(self.JWT_TOKEN)

    def test_toggle_garage_door__should_return_success_status_code(self, mock_request):
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        actual = toggle_garage_door()

        assert actual.status_code == 200

    def test_toggle_garage_door__should_return_success_headers(self, mock_request):
        expected_headers = 'text/json'
        mock_request.headers = {'Authorization': self.JWT_TOKEN}
        actual = toggle_garage_door()

        assert actual.content_type == expected_headers
