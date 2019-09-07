import os
import uuid

from svc.manager import create_app


class TestSumpRoutes:
    TEST_CLIENT = None
    JWT_SECRET = 'fakeKey'

    def setup_method(self):
        flask_app = create_app('__main__')
        self.TEST_CLIENT = flask_app.test_client()
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})

    def teardown_method(self):
        os.environ.pop('JWT_SECRET')

    def test_get_current_sump_level__should_return_not_found_when_user_does_not_exist(self):
        user_id = uuid.uuid4().hex
        url = 'sumpPump/user/' + user_id + '/depth'

        actual = self.TEST_CLIENT.get(url)

        assert actual.status_code == 400
