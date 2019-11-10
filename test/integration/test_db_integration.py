import uuid
from datetime import datetime

import pytest
from werkzeug.exceptions import BadRequest, Unauthorized

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.db.models.user_information_model import UserInformation, DailySumpPumpLevel, AverageSumpPumpLevel, \
    UserCredentials, Roles, UserPreference


# TODO: break class apart into multiple test classes
class TestDbIntegration:

    first_user_id = uuid.uuid4()
    second_user_id = uuid.uuid4()
    cred_id = uuid.uuid4()
    expected_depth = 8.0
    date = datetime.date(datetime.now())
    user_name = 'Jonny'
    password = 'fakePass'
    city = 'Praha'
    first_user_login = None
    first_user = None
    second_user = None
    first_user_preference = None
    first_sump_daily = None
    second_sump_daily = None
    third_sump_daily = None
    first_sump_average = None
    second_sump_average = None

    def setup_method(self):
        with UserDatabaseManager() as database:
            self.first_user_preference = UserPreference(user_id=self.first_user_id.hex, is_fahrenheit=True, city=self.city)
            self.first_user_login = UserCredentials(id=self.cred_id.hex, user_name=self.user_name, password=self.password, user_id=self.first_user_id.hex)
            self.first_user = UserInformation(id=self.first_user_id.hex, first_name='Jon', last_name='Test')
            self.second_user = UserInformation(id=self.second_user_id.hex, first_name='Dylan', last_name='Fake')
            self.first_sump_daily = DailySumpPumpLevel(id=88, distance=11.0, user_id=self.first_user_id.hex, warning_level=2, create_date=datetime.now())
            self.second_sump_daily = DailySumpPumpLevel(id=99, distance=self.expected_depth, user_id=self.second_user_id.hex, warning_level=1, create_date=datetime.now())
            self.third_sump_daily = DailySumpPumpLevel(id=100, distance=12.0, user_id=self.second_user_id.hex, warning_level=2, create_date=datetime.now())

            self.first_sump_average = AverageSumpPumpLevel(id=34, user_id=self.first_user_id.hex, distance=12.0, create_day=self.date)
            self.second_sump_average = AverageSumpPumpLevel(id=35, user_id=self.first_user_id.hex, distance=self.expected_depth, create_day=self.date)
            self.first_user_login.role_id = database.session.query(Roles).first().id

            database.session.add(self.first_user_login)
            database.session.add_all([self.first_user, self.second_user])
            database.session.add(self.first_user_preference)
            database.session.add_all([self.first_sump_average, self.second_sump_average])
            database.session.add_all([self.first_sump_daily, self.second_sump_daily, self.third_sump_daily])

    def teardown_method(self):
        with UserDatabaseManager() as database:
            database.session.delete(self.first_sump_daily)
            database.session.delete(self.second_sump_daily)
            database.session.delete(self.third_sump_daily)
            database.session.delete(self.first_sump_average)
            database.session.delete(self.second_sump_average)
            database.session.delete(self.first_user_login)
            database.session.delete(self.first_user_preference)
            database.session.delete(self.second_user)
            database.session.delete(self.first_user)

    def test_validate_credentials__should_return_user_id_when_user_exists(self):
        with UserDatabaseManager() as database:
            actual = database.validate_credentials(self.user_name, self.password)

            assert actual == str(self.first_user_id)

    def test_validate_credentials__should_raise_unauthorized_when_user_does_not_exist(self):
        with UserDatabaseManager() as database:
            with pytest.raises(Unauthorized):
                database.validate_credentials('missingUser', 'missingPassword')

    def test_validate_credentials__should_raise_unauthorized_when_password_does_not_match(self):
        with UserDatabaseManager() as database:
            user_pass = 'wrongPassword'
            with pytest.raises(Unauthorized):
                database.validate_credentials(self.user_name, user_pass)

    def test_get_preferences_by_user__should_return_preferences_for_valid_user(self):
        with UserDatabaseManager() as database:
            response = database.get_preferences_by_user(str(self.first_user_id))

            assert response['unit'] == 'imperial'
            assert response['city'] == self.city
            assert response['is_fahrenheit'] is True

    def test_get_preferences_by_user__should_raise_bad_request_when_no_preferences(self):
        with pytest.raises(BadRequest):
            with UserDatabaseManager() as database:
                bad_user_id = uuid.uuid4().hex
                database.get_preferences_by_user(bad_user_id)

    def test_get_current_sump_level_by_user__should_return_valid_sump_level(self):
        with UserDatabaseManager() as database:
            actual = database.get_current_sump_level_by_user(self.first_user_id.hex)
            assert actual['currentDepth'] == 11.0
            assert actual['warningLevel'] == 2

    def test_get_current_sump_level_by_user__should_return_latest_record_for_single_user(self):
        with UserDatabaseManager() as database:
            actual = database.get_current_sump_level_by_user(self.second_user_id.hex)
            assert actual['currentDepth'] == 12.0
            assert actual['warningLevel'] == 2

    def test_get_current_sump_level_by_user__should_raise_bad_request_when_user_not_found(self):
        with UserDatabaseManager() as database:
            with pytest.raises(BadRequest):
                database.get_current_sump_level_by_user(uuid.uuid4().hex)

    def test_get_average_sump_level_by_user__should_return_latest_record_for_single_user(self):
        with UserDatabaseManager() as database:
            actual = database.get_average_sump_level_by_user(self.first_user_id.hex)
            assert actual == {'averageDepth': self.expected_depth, 'latestDate': str(self.date)}

    def test_get_average_sump_level_by_user__should_raise_bad_request_when_user_not_found(self):
        with UserDatabaseManager() as database:
            with pytest.raises(BadRequest):
                database.get_average_sump_level_by_user(uuid.uuid4().hex)

    def test_insert_current_sump_level__should_store_new_record(self):
        depth = 12.345
        with UserDatabaseManager() as database:
            depth_info = {'depth': depth,
                          'warning_level': 3,
                          'datetime': str(datetime.now())}
            database.insert_current_sump_level(self.first_user_id.hex, depth_info)

            actual = database.session.query(DailySumpPumpLevel).filter_by(user_id=self.first_user_id.hex, distance=depth).first()

            assert float(actual.distance) == depth

            database.session.query(DailySumpPumpLevel).filter_by(user_id=self.first_user_id.hex, distance=depth).delete()

    def test_insert_current_sump_level__should_raise_exception_with_bad_data(self):
        depth_info = {'badData': None}
        user_id = 1234
        with pytest.raises(BadRequest):
            with UserDatabaseManager() as database:
                database.insert_current_sump_level(user_id, depth_info)
