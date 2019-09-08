import uuid
from datetime import datetime

import pytest
from werkzeug.exceptions import BadRequest, Unauthorized

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.db.models.user_information_model import UserInformation, DailySumpPumpLevel, AverageSumpPumpLevel


def test_validate_credentials__should_return_user_id_when_user_exists():
    with UserDatabaseManager() as database:
        user_info = database.session.query(UserInformation).filter_by(last_name='Tester').first()
        user_name = 'Jonny561201'
        user_pass = 'password'
        actual = database.validate_credentials(user_name, user_pass)

        assert actual == user_info.id


def test_validate_credentials__should_raise_unauthorized_when_user_does_not_exist():
    with UserDatabaseManager() as database:
        user_name = 'missingUser'
        user_pass = 'fakePassword'
        with pytest.raises(Unauthorized):
            database.validate_credentials(user_name, user_pass)


def test_validate_credentials__should_raise_unauthorized_when_password_does_not_match():
    with UserDatabaseManager() as database:
        user_name = 'l33t'
        user_pass = 'wrongPassword'
        with pytest.raises(Unauthorized):
            database.validate_credentials(user_name, user_pass)


def test_get_preferences_by_user__should_return_preferences_for_valid_user():
    with UserDatabaseManager() as database:
        user_info = database.session.query(UserInformation).filter_by(last_name='Tester').first()

        response = database.get_preferences_by_user(user_info.id)

        assert response.is_fahrenheit is True
        assert response.user_id == user_info.id


def test_get_preferences_by_user__should_raise_bad_request_when_no_preferences():
    with pytest.raises(BadRequest):
        with UserDatabaseManager() as database:
            bad_user_id = uuid.uuid4().hex
            database.get_preferences_by_user(bad_user_id)


def test_get_current_sump_level_by_user__should_return_valid_sump_level():
    expected_distance = 8.0
    first_user = UserInformation(id=uuid.uuid4().hex, first_name='Jon', last_name='Test')
    second_user = UserInformation(id=uuid.uuid4().hex, first_name='Dylan', last_name='Fake')

    first_sump = DailySumpPumpLevel(id=1, user=first_user, distance=12.0, create_date=datetime.now())
    second_sump = DailySumpPumpLevel(id=2, user=second_user, distance=expected_distance, create_date=datetime.now())

    with UserDatabaseManager() as database:
        database.session.add_all([first_sump, second_sump])
        database.session.flush()

        actual = database.get_current_sump_level_by_user(second_user.id)

        database.session.delete(first_sump)
        database.session.delete(first_user)
        database.session.delete(second_sump)
        database.session.delete(second_user)

        assert actual == expected_distance


def test_get_current_sump_level_by_user__should_return_latest_record_for_single_user():
    first_user = UserInformation(id=uuid.uuid4().hex, first_name='Jon', last_name='Test')

    first_sump = DailySumpPumpLevel(id=1, user=first_user, distance=12.0, create_date=datetime.now())
    second_sump = DailySumpPumpLevel(id=2, user=first_user, distance=8.0, create_date=datetime.now())

    with UserDatabaseManager() as database:
        database.session.add_all([first_sump, second_sump])
        database.session.flush()

        actual = database.get_current_sump_level_by_user(first_user.id)

        database.session.delete(first_user)
        database.session.delete(first_sump)
        database.session.delete(second_sump)

        assert actual == 8.0


def test_get_current_sump_level_by_user__should_raise_bad_request_when_user_not_found():
    with UserDatabaseManager() as database:
        with pytest.raises(BadRequest):
            database.get_current_sump_level_by_user(uuid.uuid4().hex)


def test_get_average_sump_level_by_user__should_return_latest_record_for_single_user():
    expected_depth = 8.0
    first_user = UserInformation(id=uuid.uuid4().hex, first_name='Jon', last_name='Test')

    date = datetime.date(datetime.now())
    first_sump = AverageSumpPumpLevel(id=1, user=first_user, distance=12.0, create_day=date)
    second_sump = AverageSumpPumpLevel(id=2, user=first_user, distance=expected_depth, create_day=date)

    with UserDatabaseManager() as database:
        database.session.add_all([first_sump, second_sump])
        database.session.flush()

        actual = database.get_average_sump_level_by_user(first_user.id)

        database.session.delete(first_user)
        database.session.delete(first_sump)
        database.session.delete(second_sump)

        assert actual == {'averageDepth': expected_depth, 'latestDate': str(date)}


def test_get_average_sump_level_by_user__should_raise_bad_request_when_user_not_found():
    with UserDatabaseManager() as database:
        with pytest.raises(BadRequest):
            database.get_average_sump_level_by_user(uuid.uuid4().hex)


def test_save_current_sump_level__should_store_new_record():
    depth = 12.345
    with UserDatabaseManager() as database:
        user_info = database.session.query(UserInformation).filter_by(last_name='Tester').first()
        depth_info = {'userId': user_info.id,
                      'depth': depth,
                      'datetime': str(datetime.now())}
        database.save_current_sump_level(depth_info)

        actual = database.session.query(DailySumpPumpLevel).filter_by(user_id=user_info.id).first()

        assert float(actual.distance) == depth

        database.session.query(DailySumpPumpLevel).filter_by(user_id=user_info.id).delete()


def test_save_current_sump_level__should_raise_exception_with_bad_data():
    depth_info = {'badData': None}
    with pytest.raises(BadRequest):
        with UserDatabaseManager() as database:
            database.save_current_sump_level(depth_info)
