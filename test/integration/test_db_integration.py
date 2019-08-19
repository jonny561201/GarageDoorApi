from svc.db.methods.user_credentials import UserDatabaseManager


def test_are_credentials_valid__should_return_true_when_user_exists():
    with UserDatabaseManager() as database:
        credentials = {'username': 'Jonny561201', 'password': 'password'}
        response = database.are_credentials_valid(credentials)

        assert response is True


def test_are_credentials_valid__should_return_false_when_user_does_not_exist():
    with UserDatabaseManager() as database:
        credentials = {'username': 'missingUser', 'password': 'fakePassword'}
        response = database.are_credentials_valid(credentials)

        assert response is False
