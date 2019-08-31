import os

from svc.manager import create_app


class TestThermostatRoutesIntegration:
    TEST_CLIENT = None
    JWT_SECRET = 'fake_secret'

    def setup_method(self):
        flask_app = create_app('__main__')
        self.TEST_CLIENT = flask_app.test_client()
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def test_get_temperature__should_return_unauthorized_error_when_invalid_user(self):
        actual = self.TEST_CLIENT.get('thermostat/temperature')

        assert actual.status_code == 401
