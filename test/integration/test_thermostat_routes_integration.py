import os
import uuid

import jwt
from flask import json

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.db.models.user_information_model import UserInformation, UserPreference
from svc.manager import create_app


class TestThermostatRoutesIntegration:
    TEST_CLIENT = None
    JWT_SECRET = 'fake_secret'
    USER_ID = None
    USER = None
    PREFERENCE = None

    def setup_method(self):
        self.USER_ID = uuid.uuid4()
        self.USER = UserInformation(id=self.USER_ID.hex, first_name='Jon', last_name='Test')
        self.PREFERENCE = UserPreference(user_id=self.USER_ID.hex, city='London', is_fahrenheit=False)
        flask_app = create_app('__main__')
        self.TEST_CLIENT = flask_app.test_client()
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})
        with UserDatabaseManager() as database:
            database.session.add(self.USER)
            database.session.add(self.PREFERENCE)

    def teardown_method(self):
        with UserDatabaseManager() as database:
            database.session.delete(self.PREFERENCE)
            database.session.delete(self.USER)

    def test_get_temperature__should_return_unauthorized_error_when_invalid_user(self):
        url = 'thermostat/temperature/' + '890234890234'
        actual = self.TEST_CLIENT.get(url)

        assert actual.status_code == 401

    def test_get_temperature__should_return_temperature(self):
        bearer_token = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        headers = {'Authorization': bearer_token}

        url = 'thermostat/temperature/' + self.USER_ID.hex
        actual = self.TEST_CLIENT.get(url, headers=headers)

        assert actual.status_code == 200
        assert set(['currentTemp', 'isFahrenheit', 'description', 'max_temp', 'min_temp', 'temp']) == set(json.loads(actual.data))
