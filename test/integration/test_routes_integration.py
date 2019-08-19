import os

import jwt

from svc.manager import create_app


class TestRouteIntegration:
    test_client = None
    JWT_SECRET = 'testSecret'

    def setup_method(self):
        flask_app = create_app('__main__')
        self.test_client = flask_app.test_client()
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self):
        os.environ.pop('JWT_SECRET')

    def test_health_check__should_return_success(self):
        actual = self.test_client.get('healthCheck')

        assert actual.status_code == 200
        assert actual.data.decode('UTF-8') == 'Success'

    def test_get_garage_door_status__should_return_unauthorized(self):
        actual = self.test_client.get('garageDoor/status')

        assert actual.status_code == 401

    def test_get_garage_door_status__should_return_success_with_valid_jwt(self):
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}
        actual = self.test_client.get('garageDoor/status', headers=headers)

        assert actual.status_code == 200
