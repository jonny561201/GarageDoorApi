import os

from svc.constants.settings_state import Settings


class TestState:
    SETTINGS = None
    JWT_SECRET = 'FakeSecret'

    def setup_method(self):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET})
        self.SETTINGS = Settings.get_instance()

    def teardown_method(self):
        os.environ.pop('JWT_SECRET')

    def test_jwt_secret__should_return_env_var_value(self):
        self.SETTINGS.dev_mode = False
        assert self.SETTINGS.jwt_secret == self.JWT_SECRET

    def test_dev_coordinates__should_return_default_value(self):
        self.SETTINGS.dev_mode = False
        assert self.SETTINGS.dev_coordinates == {'latitude': 41.5868, 'longitude': -93.6250}

    def test_dev_coordinates__should_return_dictionary_if_dev_mode(self):
        coordinates = {'latitude': 40.123, 'longitude': -93.123}
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'DevCoordinates': coordinates}
        assert self.SETTINGS.dev_coordinates == coordinates

    def test_jwt_secret__should_pull_from_dictionary_if_dev_mode(self):
        jwt_secret = 'other_secret'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'DevJwtSecret': jwt_secret}
        assert self.SETTINGS.jwt_secret == jwt_secret
