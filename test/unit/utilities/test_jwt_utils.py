import os
from datetime import datetime, timedelta

import jwt
import pytest
import pytz
from mock import patch
from werkzeug.exceptions import Unauthorized

from svc.utilities.jwt_utils import is_jwt_valid, create_jwt_token


class TestJwt:
    JWT_BODY = None
    JWT_SECRET = 'testSecret'

    def setup_method(self):
        self.JWT_BODY = {'fakeBody': 'valueValue'}
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self):
        os.environ.pop('JWT_SECRET')

    def test_is_jwt_valid__should_not_fail_if_it_can_be_decrypted(self):
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
        jwt_token = 'Bearer ' + jwt.encode(jwt_body, self.JWT_SECRET, algorithm='HS256').decode('UTF-8')

        is_jwt_valid(jwt_token)

    @patch('svc.utilities.jwt_utils.datetime')
    def test_create_jwt_token__should_return_a_valid_token(self, mock_date):
        now = datetime.now(pytz.timezone('US/Central'))
        mock_date.now.return_value = now
        expected_expiration = now + timedelta(hours=2)
        truncated_expiration = (str(expected_expiration.timestamp() * 1000))[:10]
        expected_token_body = {'user_id': 12345, 'exp': int(truncated_expiration)}

        actual = create_jwt_token()

        assert jwt.decode(actual, self.JWT_SECRET, algorithms='HS256') == expected_token_body


def test_is_jwt_valid__should_return_false_if_secret_is_not_set():
    jwt_body = {'fakeBody': 'valueValue'}
    jwt_secret = 'testSecret'
    jwt_token = jwt.encode(jwt_body, jwt_secret, algorithm='HS256').decode('UTF-8')

    with pytest.raises(Unauthorized):
        is_jwt_valid(jwt_token)
