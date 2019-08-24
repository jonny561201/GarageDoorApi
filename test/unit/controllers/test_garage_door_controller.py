import json
import os
from datetime import datetime, timedelta

import jwt
import pytest
import pytz
from mock import patch
from werkzeug.exceptions import Unauthorized

from svc.controllers.garage_door_controller import get_login, get_status


@patch('svc.controllers.garage_door_controller.extract_credentials')
class TestAppRoutes:
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')
    USER = 'user_name'
    PWORD = 'password'

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    @patch('svc.controllers.garage_door_controller.UserDatabaseManager')
    def test_garage_door_login__should_raise_unauthorized_exception(self, mock_credentials, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        mock_credentials.return_value.__enter__.return_value.are_credentials_valid.return_value = False

        with pytest.raises(Unauthorized):
            get_login(self.JWT_TOKEN)

    @patch('svc.controllers.garage_door_controller.UserDatabaseManager')
    def test_garage_door_login__should_call_validate_credentials_with_post_body(self, mock_credentials, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        get_login(self.JWT_TOKEN)

        mock_credentials.return_value.__enter__.return_value.are_credentials_valid.assert_called_with(self.USER, self.PWORD)

    @patch('svc.controllers.garage_door_controller.UserDatabaseManager')
    def test_garage_door_login__should_call_extract_credentials(self, mock_credentials, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        get_login(self.JWT_TOKEN)

        mock_extract.assert_called_with(self.JWT_TOKEN)

    @patch('svc.controllers.garage_door_controller.create_jwt_token')
    @patch('svc.controllers.garage_door_controller.UserDatabaseManager')
    def test_garage_door_login__should_call_create_jwt_token(self, mock_credentials, mock_token, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        get_login(self.JWT_TOKEN)

        mock_token.assert_called()

    @patch('svc.controllers.garage_door_controller.create_jwt_token')
    @patch('svc.controllers.garage_door_controller.UserDatabaseManager')
    def test_garage_door_login__should_return_response_from_jwt_service(self, mock_credentials, mock_token, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        mock_token.return_value = self.JWT_TOKEN
        actual = get_login(self.JWT_TOKEN)

        assert actual == self.JWT_TOKEN

    @patch('svc.utilities.jwt_utils.datetime')
    @patch('svc.controllers.garage_door_controller.UserDatabaseManager')
    def test_garage_door_login__should_respond_with_jwt_token(self, mock_credentials, mock_datetime, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        now = datetime.now(tz=pytz.timezone('US/Central'))
        mock_datetime.now.return_value = now
        mock_credentials.return_value.__enter__.return_value.are_credentials_valid.return_value = True
        expected_expire = now + timedelta(hours=2)
        truncated_date = (str(expected_expire.timestamp() * 1000))[:10]
        expected_token = {'user_id': 12345, 'exp': int(truncated_date)}

        actual = get_login("junkToken")

        assert jwt.decode(actual, self.JWT_SECRET, algorithms=["HS256"]) == expected_token

    @patch('svc.controllers.garage_door_controller.garage_door_status')
    def test_garage_door_status__should_call_get_garage_door_status(self, mock_gpio, mock_extract):
        mock_gpio.return_value = {}
        get_status(self.JWT_TOKEN)

        mock_gpio.assert_called()

    def test_garage_door_status__should_return_status(self, mock_extract):
        expected_body = {"isGarageOpen": True}

        actual = get_status(self.JWT_TOKEN)
        json_actual = json.loads(actual)

        assert json_actual == expected_body

    @patch('svc.controllers.garage_door_controller.is_jwt_valid')
    def test_garage_door_status__should_call_is_jwt_valid(self, mock_validate, mock_extract):
        get_status(self.JWT_TOKEN)

        mock_validate.assert_called_with(self.JWT_TOKEN)

    def test_garage_door_status__should_raise_unauthorized_if_provided_bad_jwt(self, mock_extract):
        jwt_token = jwt.encode({'user_id': 12345}, 'bad_secret', algorithm='HS256').decode('UTF-8')
        with pytest.raises(Unauthorized):
            get_status(jwt_token)

    def test_garage_door_status__should_raise_unauthorized_if_provided_no_token(self, mock_extract):
        with pytest.raises(Unauthorized):
            get_status(None)
