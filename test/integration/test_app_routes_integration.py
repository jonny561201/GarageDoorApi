import base64
import os

from svc.manager import create_app


class TestAppRoutesIntegration:
    TEST_CLIENT = None
    JWT_SECRET = 'testSecret'

    def setup_method(self):
        flask_app = create_app('__main__')
        self.TEST_CLIENT = flask_app.test_client()
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self):
        os.environ.pop('JWT_SECRET')

    def test_health_check__should_return_success(self):
        actual = self.TEST_CLIENT.get('healthCheck')

        assert actual.status_code == 200
        assert actual.data.decode('UTF-8') == 'Success'

    def test_garage_door_login__should_return_400_when_no_header(self):
        actual = self.TEST_CLIENT.get('login')

        assert actual.status_code == 400

    def test_garage_door_login__should_return_401_when_invalid_user(self):
        user_name = 'not_real_user'
        user_pass = 'wrongPass'
        creds = "%s:%s" % (user_name, user_pass)
        headers = {'Authorization': base64.b64encode(creds.encode())}

        actual = self.TEST_CLIENT.get('login', headers=headers)

        assert actual.status_code == 401

    def test_garage_door_login__should_return_401_when_invalid_password(self):
        user_name = 'Jonny561201'
        user_pass = 'wrongPass'
        creds = "%s:%s" % (user_name, user_pass)
        headers = {'Authorization': base64.b64encode(creds.encode())}

        actual = self.TEST_CLIENT.get('login', headers=headers)

        assert actual.status_code == 401

    def test_garage_door_login__should_return_200_when_user_valid(self):
        user_name = 'Jonny561201'
        user_pass = 'password'
        creds = "%s:%s" % (user_name, user_pass)
        headers = {'Authorization': base64.b64encode(creds.encode())}

        actual = self.TEST_CLIENT.get('login', headers=headers)

        assert actual.status_code == 200
