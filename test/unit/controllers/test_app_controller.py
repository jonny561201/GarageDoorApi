import os
import uuid
from datetime import datetime, timedelta

import jwt
import pytz
from mock import patch

from svc.controllers.app_controller import get_login, get_user_preferences


@patch('svc.controllers.app_controller.extract_credentials')
@patch('svc.controllers.app_controller.UserDatabaseManager')
class TestLoginController:
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')
    USER = 'user_name'
    PWORD = 'password'
    USER_ID = 'fake_user_id'

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    @patch('svc.controllers.app_controller.create_jwt_token')
    def test_get_login__should_call_validate_credentials_with_post_body(self, mock_token, mock_credentials, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        get_login(self.JWT_TOKEN)

        mock_credentials.return_value.__enter__.return_value.validate_credentials.assert_called_with(self.USER, self.PWORD)

    @patch('svc.controllers.app_controller.create_jwt_token')
    def test_get_login__should_call_extract_credentials(self, mock_token, mock_credentials, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        get_login(self.JWT_TOKEN)

        mock_extract.assert_called_with(self.JWT_TOKEN)

    @patch('svc.controllers.app_controller.create_jwt_token')
    def test_get_login__should_call_create_jwt_token(self, mock_token, mock_credentials, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        get_login(self.JWT_TOKEN)

        mock_token.assert_called()

    @patch('svc.controllers.app_controller.create_jwt_token')
    def test_get_login__should_return_response_from_jwt_service(self, mock_token, mock_credentials, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        mock_token.return_value = self.JWT_TOKEN
        actual = get_login(self.JWT_TOKEN)

        assert actual == self.JWT_TOKEN

    @patch('svc.utilities.jwt_utils.datetime')
    def test_get_login__should_respond_with_jwt_token(self, mock_datetime, mock_db, mock_extract):
        mock_extract.return_value = (self.USER, self.PWORD)
        now = datetime.now(tz=pytz.timezone('US/Central'))
        mock_datetime.now.return_value = now
        user_id = uuid.uuid4().hex
        mock_db.return_value.__enter__.return_value.validate_credentials.return_value = user_id
        expected_expire = now + timedelta(hours=2)
        truncated_date = (str(expected_expire.timestamp() * 1000))[:10]
        expected_token = {'user_id': user_id, 'exp': int(truncated_date)}

        actual = get_login("junkToken")

        assert jwt.decode(actual, self.JWT_SECRET, algorithms=["HS256"]) == expected_token

    @patch('svc.controllers.app_controller.is_jwt_valid')
    def test_get_user_preferences__should_validate_bearer_token(self, mock_jwt, mock_db, mock_creds):
        get_user_preferences(self.JWT_SECRET, self.USER_ID)

        mock_jwt.assert_called_with(self.JWT_SECRET)

    @patch('svc.controllers.app_controller.is_jwt_valid')
    def test_get_user_preferences__should_call_get_preferences_by_user(self, mock_jwt, mock_db, mock_creds):
        get_user_preferences(self.JWT_SECRET, self.USER_ID)

        mock_db.return_value.__enter__.return_value.get_preferences_by_user.assert_called_with(self.USER_ID)

    @patch('svc.controllers.app_controller.is_jwt_valid')
    def test_get_user_preferences__should_return_preferences_response(self, mock_jwt, mock_db, mock_creds):
        expected_preferences = {'unit': 'imperial', 'city': 'Des Moines'}
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = expected_preferences

        actual = get_user_preferences(self.JWT_SECRET, self.USER_ID)

        assert actual == expected_preferences