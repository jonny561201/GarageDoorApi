import uuid

import pytest
from mock import mock
from sqlalchemy import orm
from werkzeug.exceptions import BadRequest, Unauthorized

from svc.db.methods.user_credentials import UserDatabase
from svc.db.models.user_information_model import UserPreference
from svc.db.models.user_login import UserCredentials


class TestUserDatabase:
    FAKE_USER = 'testName'
    FAKE_PASS = 'testPass'
    SESSION = None
    DATABASE = None

    def setup_method(self, _):
        self.SESSION = mock.create_autospec(orm.scoped_session)
        self.DATABASE = UserDatabase(self.SESSION)

    def test_are_credentials_valid__should_query_database_by_user_name(self):
        user = self._create_database_user()
        self.SESSION.query.return_value.filter_by.return_value.first.return_value = user

        self.DATABASE.are_credentials_valid(self.FAKE_USER, self.FAKE_PASS)

        self.SESSION.query.return_value.filter_by.assert_called_with(user_name=self.FAKE_USER)

    def test_are_credentials_valid__should_return_true_if_password_matches_queried_user(self):
        user = self._create_database_user()
        self.SESSION.query.return_value.filter_by.return_value.first.return_value = user

        self.DATABASE.are_credentials_valid(self.FAKE_USER, self.FAKE_PASS)

    def test_are_credentials_valid__should_raise_unauthorized_if_password_does_not_match_queried_user(self):
        user = self._create_database_user(password='mismatchedPass')
        self.SESSION.query.return_value.filter_by.return_value.first.return_value = user

        with pytest.raises(Unauthorized):
            self.DATABASE.are_credentials_valid(self.FAKE_USER, self.FAKE_PASS)

    def test_are_credentials_valid__should_raise_unauthorized_if_user_not_found(self):
        user = None
        self.SESSION.query.return_value.filter_by.return_value.first.return_value = user

        with pytest.raises(Unauthorized):
            self.DATABASE.are_credentials_valid(self.FAKE_USER, self.FAKE_PASS)

    def test_get_preferences_by_user__should_return_user_preferences(self):
        user = TestUserDatabase._create_database_user()
        preference = TestUserDatabase._create_user_preference(user)
        self.SESSION.query.return_value.filter_by.return_value.first.return_value = preference

        actual = self.DATABASE.get_preferences_by_user(uuid.uuid4())

        assert actual == preference

    def test_get_preferences_by_user__should_throw_bad_request_when_no_preferences(self):
        self.SESSION.query.return_value.filter_by.return_value.first.return_value = None

        with pytest.raises(BadRequest):
            self.DATABASE.get_preferences_by_user(uuid.uuid4().hex)

    @staticmethod
    def _create_user_preference(user):
        preference = UserPreference()
        preference.user = user
        return preference

    @staticmethod
    def _create_database_user(user=FAKE_USER, password=FAKE_PASS):
        return UserCredentials(id=uuid.uuid4(), user_name=user, password=password)
