import os

from svc.constants.settings_state import Settings


class TestState:
    SETTINGS = None
    JWT_SECRET = 'FakeSecret'
    FILE_NAME = 'test.json'

    def setup_method(self):
        os.environ.update({'JWT_SECRET': self.JWT_SECRET, 'FILE_NAME': self.FILE_NAME})
        self.SETTINGS = Settings.get_instance()

    def teardown_method(self):
        try:
            os.environ.pop('JWT_SECRET')
            os.environ.pop('FILE_NAME')
        except KeyError:
            print('\nEnv vars already removed')

    def test_jwt_secret__should_return_env_var_value(self):
        self.SETTINGS.dev_mode = False
        assert self.SETTINGS.jwt_secret == self.JWT_SECRET

    def test_file_name__should_return_env_var_value(self):
        self.SETTINGS.dev_mode = False
        assert self.SETTINGS.file_name == self.FILE_NAME

    def test_dev_coordinates__should_return_default_value(self):
        self.SETTINGS.dev_mode = False
        assert self.SETTINGS.dev_coordinates == {'latitude': 41.621191, 'longitude': -93.831609}

    def test_file_name__should_provide_default_name_when_environment_variable_not_set(self):
        os.environ.pop('FILE_NAME')
        self.SETTINGS.dev_mode = False
        assert self.SETTINGS.file_name == 'garageStatus.json'

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

    def test_file_name__should_pull_from_dictionary_if_dev_mode(self):
        file_name = 'other_file.json'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'FileName': file_name}
        assert self.SETTINGS.file_name == file_name
