import os

import jwt
from flask import json

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.db.models.user_information_model import UserInformation
from svc.manager import create_app


class TestThermostatRoutesIntegration:
    TEST_CLIENT = None
    JWT_SECRET = 'fake_secret'

    def setup_method(self):
        flask_app = create_app('__main__')
        self.TEST_CLIENT = flask_app.test_client()
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def test_get_temperature__should_return_unauthorized_error_when_invalid_user(self):
        url = 'thermostat/temperature/' + '890234890234'
        actual = self.TEST_CLIENT.get(url)

        assert actual.status_code == 401

    def test_get_temperature__should_return_temperature(self):
        with UserDatabaseManager() as database:
            user = database.session.query(UserInformation).filter_by(last_name='Tester').first()

            bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
            headers = {'Authorization': bearer_token}

            url = 'thermostat/temperature/' + user.id
            actual = self.TEST_CLIENT.get(url, headers=headers)

            assert actual.status_code == 200
            assert set(['currentTemp', 'isFahrenheit', 'description', 'max_temp', 'min_temp', 'temp']) == set(json.loads(actual.data))
