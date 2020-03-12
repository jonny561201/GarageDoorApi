import os
from datetime import datetime, timedelta

import jwt
import pytest
from mock import patch
from werkzeug.exceptions import Unauthorized

from svc.utilities.jwt_utils import is_jwt_valid


@patch('svc.utilities.jwt_utils.Settings')
class TestJwt:
    JWT_BODY = None
    JWT_SECRET = 'testSecret'

    def setup_method(self):
        self.JWT_BODY = {'fakeBody': 'valueValue'}
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self):
        os.environ.pop('JWT_SECRET')

    def test_is_jwt_valid__should_not_fail_if_it_can_be_decrypted(self, mock_settings):
        mock_settings.get_instance.return_value.get_settings.return_value = {}
        jwt_token = jwt.encode(self.JWT_BODY, self.JWT_SECRET, algorithm='HS256').decode('UTF-8')

        is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_raise_unauthorized_if_it_cannot_be_decrypted(self, mock_settings):
        mock_settings.get_instance.return_value.get_settings.return_value = {}
        jwt_token = jwt.encode(self.JWT_BODY, 'badSecret', algorithm='HS256').decode('UTF-8')

        with pytest.raises(Unauthorized):
            is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_raise_unauthorized_if_token_has_expired(self, mock_settings):
        mock_settings.get_instance.return_value.get_settings.return_value = {}
        expired_date = datetime.now() - timedelta(hours=1)
        self.JWT_BODY['exp'] = expired_date
        jwt_token = jwt.encode(self.JWT_BODY, self.JWT_SECRET, algorithm='HS256').decode('UTF-8')

        with pytest.raises(Unauthorized):
            is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_raise_unauthorized_if_token_is_none(self, mock_settings):
        jwt_token = None

        with pytest.raises(Unauthorized):
            is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_raise_unauthorized_if_token_is_invalid_string(self, mock_settings):
        mock_settings.get_instance.return_value.get_settings.return_value = {'Development': False}
        jwt_token = 'abc123'

        with pytest.raises(Unauthorized):
            is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_succeed_when_provided_bearer_text_in_token(self, mock_settings):
        mock_settings.get_instance.return_value.get_settings.return_value = {}
        jwt_body = {'fakeBody': 'valueValue'}
        jwt_token = 'Bearer ' + jwt.encode(jwt_body, self.JWT_SECRET, algorithm='HS256').decode('UTF-8')

        is_jwt_valid(jwt_token)

    def test_is_jwt_valid__should_succeed_using_secret_from_settings_to_encode_token(self, mock_settings):
        mock_settings.get_instance.return_value.get_settings.return_value = {'Development': True}
        jwt_body = {'fakeBody': 'valueValue'}
        jwt_token = 'Bearer ' + jwt.encode(jwt_body, "", algorithm='HS256').decode('UTF-8')

        is_jwt_valid(jwt_token)


@patch('svc.utilities.jwt_utils.Settings')
def test_is_jwt_valid__should_raise_exception_if_secret_is_not_set(mock_settings):
    mock_settings.get_instance.return_value.get_settings.return_value = {}
    jwt_body = {'fakeBody': 'valueValue'}
    jwt_secret = 'testSecret'
    jwt_token = jwt.encode(jwt_body, jwt_secret, algorithm='HS256').decode('UTF-8')

    with pytest.raises(Unauthorized):
        is_jwt_valid(jwt_token)
