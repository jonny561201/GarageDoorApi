import json
import os

import jwt
from mock import patch, ANY

from svc.controllers.app_controller import get_login, get_user_preferences, save_user_preferences


@patch('svc.controllers.app_controller.UserDatabaseManager')
@patch('svc.controllers.app_controller.jwt_utils')
class TestLoginController:
    AUTH_TOKEN = 'not_a_real_auth_token'
    JWT_SECRET = 'fake_jwt_secret'
    JWT_TOKEN = jwt.encode({}, JWT_SECRET, algorithm='HS256').decode('UTF-8')
    USER = 'user_name'
    PWORD = 'password'
    USER_ID = 'fake_user_id'

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    def test_get_login__should_call_validate_credentials_with_post_body(self, mock_jw, mock_db):
        mock_jw.extract_credentials.return_value = (self.USER, self.PWORD)
        get_login(self.AUTH_TOKEN)

        mock_db.return_value.__enter__.return_value.validate_credentials.assert_called_with(self.USER, self.PWORD)

    def test_get_login__should_call_extract_credentials(self, mock_jw, mock_db):
        mock_jw.extract_credentials.return_value = (self.USER, self.PWORD)
        get_login(self.AUTH_TOKEN)

        mock_jw.extract_credentials.assert_called_with(self.AUTH_TOKEN)

    def test_get_login__should_call_create_jwt_token(self, mock_jw, mock_db):
        mock_jw.extract_credentials.return_value = (self.USER, self.PWORD)
        get_login(self.AUTH_TOKEN)

        mock_jw.create_jwt_token.assert_called()

    def test_get_login__should_return_response_from_jwt_service(self, mock_jw, mock_db):
        mock_jw.extract_credentials.return_value = (self.USER, self.PWORD)
        mock_jw.create_jwt_token.return_value = self.JWT_TOKEN
        actual = get_login(self.AUTH_TOKEN)

        assert actual == self.JWT_TOKEN

    def test_get_user_preferences__should_validate_bearer_token(self, mock_jw, mock_db):
        get_user_preferences(self.AUTH_TOKEN, self.USER_ID)

        mock_jw.is_jwt_valid.assert_called_with(self.AUTH_TOKEN)

    def test_get_user_preferences__should_call_get_preferences_by_user(self, mock_jw, mock_db):
        get_user_preferences(self.AUTH_TOKEN, self.USER_ID)

        mock_db.return_value.__enter__.return_value.get_preferences_by_user.assert_called_with(self.USER_ID)

    def test_get_user_preferences__should_return_preferences_response(self, mock_jw, mock_db):
        expected_preferences = {'unit': 'imperial', 'city': 'Des Moines'}
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = expected_preferences

        actual = get_user_preferences(self.AUTH_TOKEN, self.USER_ID)

        assert actual == expected_preferences

    def test_save_user_preferences__should_validate_bearer_token(self, mock_jw, mock_db):
        bearer_token = 'fakeBearerToken'
        request_data = json.dumps({}).encode()

        save_user_preferences(bearer_token, self.USER_ID, request_data)

        mock_jw.is_jwt_valid.assert_called_with(bearer_token)

    def test_save_user_preferences__should_call_insert_preferences_by_user_with_user_id(self, mock_jw, mock_db):
        bearer_token = 'fakeBearerToken'
        request_data = json.dumps({}).encode()

        save_user_preferences(bearer_token, self.USER_ID, request_data)

        mock_db.return_value.__enter__.return_value.insert_preferences_by_user.assert_called_with(self.USER_ID, ANY)

    def test_save_user_preferences__should_call_insert_preferences_by_user_with_user_info(self, mock_jw, mock_db):
        bearer_token = 'fakeBearerToken'
        user_preferences = {'city': 'Berlin'}
        request_data = json.dumps(user_preferences).encode('UTF-8')

        save_user_preferences(bearer_token, self.USER_ID, request_data)

        mock_db.return_value.__enter__.return_value.insert_preferences_by_user.assert_called_with(ANY, user_preferences)
