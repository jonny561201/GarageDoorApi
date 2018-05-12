import os

import jwt
from svc.utilities.jwt_utils import is_jwt_valid


class TestJwt():
    JWT_BODY = {'fakeBody': 'valueValue'}
    JWT_SECRET = 'testSecret'

    def setup_method(self, _):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self, _):
        os.environ.pop('JWT_SECRET')

    def test_is_jwt_valid__should_return_true_if_it_can_be_decrypted(self):
        jwt_token = jwt.encode(self.JWT_BODY, self.JWT_SECRET, algorithm='HS256')

        acutal = is_jwt_valid(jwt_token)

        assert acutal is True

    def test_is_jwt_valid__should_return_false_if_it_cannot_be_decrypted(self):
        jwt_token = jwt.encode(self.JWT_BODY, 'badSecret', algorithm='HS256')

        acutal = is_jwt_valid(jwt_token)

        assert acutal is False
