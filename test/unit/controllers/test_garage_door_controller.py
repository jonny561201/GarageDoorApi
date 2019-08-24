import os
from datetime import datetime, timedelta

import jwt
import pytest
import pytz
from mock import patch
from werkzeug.exceptions import Unauthorized

from svc.controllers.garage_door_controller import get_login


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
