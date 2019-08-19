import uuid

from mock import mock
from sqlalchemy import orm

from svc.db.methods.user_credentials import UserDatabase
from svc.db.models.user_models import UserCredentials


class TestUserDatabase:
    FAKE_USER = 'testName'
    FAKE_PASS = 'testPass'
    CREDENTIALS = {'username': FAKE_USER, 'password': FAKE_PASS}
    SESSION = None
    DATABASE = None

    def setup_method(self, _):
        self.SESSION = mock.create_autospec(orm.scoped_session)
        self.DATABASE = UserDatabase(self.SESSION)

    def test_user_credentials_are_valid__should_query_database_by_user_name(self):

        self.DATABASE.user_credentials_are_valid(self.CREDENTIALS)

        expected_user_name = self.CREDENTIALS['username']
        self.SESSION.query.return_value.filter_by.assert_called_with(user_name=expected_user_name)

    def test_user_credentials_are_valid__should_return_true_if_password_matches_queried_user(self):
        user = self._create_database_user()
        self.SESSION.query.return_value.filter_by.return_value.first.return_value = user

        actual = self.DATABASE.user_credentials_are_valid(self.CREDENTIALS)

        assert actual is True

    def test_user_credentials_are_valid__should_return_false_if_password_does_not_match_queried_user(self):
        user = self._create_database_user(password='mismatchedPass')
        self.SESSION.query.return_value.filter_by.return_value.first.return_value = user

        actual = self.DATABASE.user_credentials_are_valid(self.CREDENTIALS)

        assert actual is False

    @staticmethod
    def _create_database_user(user=FAKE_USER, password=FAKE_PASS):
        return UserCredentials(user_key=uuid.uuid4(), user_name=user, password=password)
