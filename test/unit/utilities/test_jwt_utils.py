import os
from datetime import datetime, timedelta

import jwt
import pytz
from mock import patch

from svc.utilities.jwt_utils import is_jwt_valid, create_jwt_token


class TestJwt():
    JWT_BODY = None
    JWT_SECRET = 'testSecret'

    def setup_method(self, _):
        self.JWT_BODY = {'fakeBody': 'valueValue'}
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    def test_is_jwt_valid__should_return_true_if_it_can_be_decrypted(self):
        jwt_token = jwt.encode(self.JWT_BODY, self.JWT_SECRET, algorithm='HS256')

        acutal = is_jwt_valid(jwt_token)

        assert acutal is True

    def test_is_jwt_valid__should_return_false_if_it_cannot_be_decrypted(self):
        jwt_token = jwt.encode(self.JWT_BODY, 'badSecret', algorithm='HS256')

        actual = is_jwt_valid(jwt_token)

        assert actual is False

    def test_is_jwt_valid__should_return_false_if_token_has_expired(self):
        expired_date = datetime.now() - timedelta(hours=1)
        self.JWT_BODY['exp'] = expired_date
        jwt_token = jwt.encode(self.JWT_BODY, self.JWT_SECRET, algorithm='HS256')

        actual = is_jwt_valid(jwt_token)

        assert actual is False

    def test_is_jwt_valid__should_return_false_if_token_is_none(self):
        jwt_token = None

        actual = is_jwt_valid(jwt_token)

        assert actual is False

    def test_is_jwt_valid__should_return_false_if_token_is_invalid_string(self):
        jwt_token = 'abc123'

        actual = is_jwt_valid(jwt_token)

        assert actual is False

    @patch('svc.utilities.jwt_utils.datetime')
    def test_create_jwt_token__should_return_a_valid_token(self, mock_date):
        now = datetime.now(pytz.timezone('US/Central'))
        mock_date.now.return_value = now
        expected_expiration = now + timedelta(hours=2)
        truncated_expiration = (str(expected_expiration.timestamp() * 1000))[:10]
        expected_token_body = {'user_id': 12345, 'exp': int(truncated_expiration)}

        actual = create_jwt_token()

        assert jwt.decode(actual, self.JWT_SECRET, algorithms='HS256') == expected_token_body
