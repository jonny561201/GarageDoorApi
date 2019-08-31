from svc.db.methods.user_credentials import UserDatabaseManager
from svc.db.models.user_information_model import UserInformation


def test_are_credentials_valid__should_return_true_when_user_exists():
    with UserDatabaseManager() as database:
        user_name = 'Jonny561201'
        user_pass = 'password'
        response = database.are_credentials_valid(user_name, user_pass)

        assert response is True


def test_are_credentials_valid__should_return_false_when_user_does_not_exist():
    with UserDatabaseManager() as database:
        user_name = 'missingUser'
        user_pass = 'fakePassword'
        response = database.are_credentials_valid(user_name, user_pass)

        assert response is False


def test_are_credentials_valid__should_return_false_when_password_does_not_match():
    with UserDatabaseManager() as database:
        user_name = 'l33t'
        user_pass = 'wrongPassword'
        response = database.are_credentials_valid(user_name, user_pass)

        assert response is False


def test_get_preferences_by_user__should_return_preferences_for_valid_user():
    with UserDatabaseManager() as database:
        user_info = database.session.query(UserInformation).filter_by(last_name='Tester').first()

        response = database.get_preferences_by_user(user_info.id)

        assert response.is_fahrenheit is True
        assert response.user_id == user_info.id
