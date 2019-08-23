from svc.db.methods.user_credentials import UserDatabaseManager


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
