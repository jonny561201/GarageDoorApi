import os

from svc.config.settings_state import Settings


class TestStateEnvVar:
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
        assert self.SETTINGS.jwt_secret == self.JWT_SECRET

    def test_file_name__should_return_env_var_value(self):
        self.SETTINGS._settings = None
        assert self.SETTINGS.file_name == self.FILE_NAME

    def test_file_name__should_provide_default_name_when_environment_variable_not_set(self):
        os.environ.pop('FILE_NAME')
        assert self.SETTINGS.file_name == 'garageStatus.json'


class TestSettingsState:
    COORDINATES = {'latitude': 40.123, 'longitude': -93.123}
    VALUES = {'FileName': 'other_file.json', 'JwtSecret': 'other_secret', 'Environment': 'test'}

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        self.SETTINGS._settings = self.VALUES
        self.SETTINGS.Coordinates._settings = self.COORDINATES

    def test_environment__should_return(self):
        assert self.SETTINGS.environment == self.VALUES['Environment']

    def test_environment__should_default_to_local(self):
        self.SETTINGS._settings = None
        assert self.SETTINGS.environment == 'local'

    def test_coordinates__should_return(self):
        assert self.SETTINGS.Coordinates.latitude == self.COORDINATES['latitude']
        assert self.SETTINGS.Coordinates.longitude == self.COORDINATES['longitude']

    def test_jwt_secret__should_return(self):
        assert self.SETTINGS.jwt_secret == self.VALUES['JwtSecret']

    def test_file_name__should_return(self):
        assert self.SETTINGS.file_name == self.VALUES['FileName']
