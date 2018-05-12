from mock import mock
from sqlalchemy import orm

from svc.db.methods.user_credentials import UserDatabase


class TestUserDatabase():
    SESSION = None
    DATABASE = None

    def setup_method(self):
        self.SESSION = mock.create_autospec(orm.scoped_session)
        self.DATABASE = UserDatabase(self.SESSION)

    def test_user_credentials_are_valid__should_query_database(self):
        credentials = {'username': 'testName', 'password': 'testPass'}
        self.DATABASE.user_credentials_are_valid(credentials)

        expected_user_name = credentials['username']
        self.SESSION.query.return_value.filter_by.assert_called_with(user_name=expected_user_name)