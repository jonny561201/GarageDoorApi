import os
from datetime import datetime, timedelta

import jwt
import pytest
from werkzeug.exceptions import Unauthorized

from svc.config.settings_state import Settings
from svc.utilities.jwt_utils import is_jwt_valid


class TestJwt:
    JWT_BODY = None
    JWT_SECRET = 'testSecret'

    def setup_method(self):
        self.JWT_BODY = {'fakeBody': 'valueValue'}
        self.SETTINGS = Settings.get_instance()
        self.SETTINGS._settings = {'JwtSecret': self.JWT_SECRET}

    def test_is_jwt_valid__should_succeed_if_token_can_be_decrypted(self):
        jwt_token = jwt.encode(self.JWT_BODY, self.JWT_SECRET, algorithm='HS256').decode('UTF-8')

        is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_raise_unauthorized_if_it_cannot_be_decrypted(self):
        jwt_token = jwt.encode(self.JWT_BODY, 'badSecret', algorithm='HS256').decode('UTF-8')

        with pytest.raises(Unauthorized):
            is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_raise_unauthorized_if_token_has_expired(self):
        expired_date = datetime.now() - timedelta(hours=1)
        self.JWT_BODY['exp'] = expired_date
        jwt_token = jwt.encode(self.JWT_BODY, self.JWT_SECRET, algorithm='HS256').decode('UTF-8')

        with pytest.raises(Unauthorized):
            is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_raise_unauthorized_if_token_is_none(self):
        jwt_token = None

        with pytest.raises(Unauthorized):
            is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_raise_unauthorized_if_token_is_invalid_string(self):
        jwt_token = 'abc123'

        with pytest.raises(Unauthorized):
            is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_succeed_when_provided_bearer_text_in_token(self):
        jwt_body = {'fakeBody': 'valueValue'}
        token = jwt.encode(jwt_body, self.JWT_SECRET, algorithm='HS256').decode('UTF-8')
        bearer_token = f'Bearer {token}'

        is_jwt_valid(bearer_token)

    def test_is_jwt_valid__should_succeed_using_secret_from_settings_to_encode_token(self):
        jwt_body = {'fakeBody': 'valueValue'}
        token = jwt.encode(jwt_body, self.JWT_SECRET, algorithm='HS256').decode('UTF-8')

        is_jwt_valid(token)

    def test_is_jwt_valid__should_raise_exception_if_secret_is_not_set(self):
        os.environ.update({'JWT_SECRET': ''})
        jwt_body = {'fakeBody': 'valueValue'}
        jwt_secret = 'testSecret'
        jwt_token = jwt.encode(jwt_body, jwt_secret, algorithm='HS256').decode('UTF-8')

        with pytest.raises(Unauthorized):
            is_jwt_valid(jwt_token)
