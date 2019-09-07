import os
import uuid
from datetime import datetime

import jwt

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.db.models.user_information_model import UserInformation, DailySumpPumpLevel
from svc.manager import create_app


class TestSumpRoutes:
    TEST_CLIENT = None
    JWT_SECRET = 'fakeKey'

    def setup_method(self):
        flask_app = create_app('__main__')
        self.TEST_CLIENT = flask_app.test_client()
        self.BEAR_TOKEN = jwt.encode({}, self.JWT_SECRET, algorithm='HS256')
        self.HEADER = {'Authorization': 'Bearer ' + self.BEAR_TOKEN.decode('UTF-8')}
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self):
        os.environ.pop('JWT_SECRET')

    def test_get_current_sump_level__should_return_not_found_when_user_does_not_exist(self):
        user_id = uuid.uuid4().hex
        url = 'sumpPump/user/' + user_id + '/depth'

        actual = self.TEST_CLIENT.get(url, headers=self.HEADER)

        assert actual.status_code == 400

    def test_get_current_sump_level__should_raise_unauthorized_when_invalid_user(self):
        user_id = uuid.uuid4().hex
        url = 'sumpPump/user/' + user_id + '/depth'

        actual = self.TEST_CLIENT.get(url, headers={})

        assert actual.status_code == 401

    def test_get_current_sump_level__should_return_valid_response(self):
        user_id = uuid.uuid4().hex
        user = UserInformation(id=user_id, first_name='Jon', last_name='Test')
        sump = DailySumpPumpLevel(user=user, id=5, user_id=user_id, distance=12.45, create_date=datetime.now())
        with UserDatabaseManager() as database:
            database.session.add(sump)
            database.session.flush()

        url = 'sumpPump/user/' + user_id + '/depth'

        actual = self.TEST_CLIENT.get(url, headers=self.HEADER)

        with UserDatabaseManager() as database:
            database.session.delete(sump)
            database.session.delete(user)
            database.session.flush()

        assert actual.status_code == 200


