import json
import os

from svc.config.singleton import Singleton


@Singleton
class Settings:
    _settings = None

    def __init__(self):
        self.__get_settings()
        self.Coordinates = Coordinates(self._settings)

    @property
    def environment(self):
        return self._settings.get('Environment') if self._settings is not None else 'local'

    @property
    def jwt_secret(self):
        return os.environ.get('JWT_SECRET') if os.environ.get('JWT_SECRET') is not None else self._settings.get('JwtSecret')

    @property
    def file_name(self):
        return self._settings.get('FileName') if self._settings is not None else 'garageStatus.json'

    def __get_settings(self):
        try:
            environment = os.environ.get('PYTHON_ENVIRONMENT', 'local')
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', f'settings.{environment}.json')
            with open(file_path, "r") as reader:
                self._settings = json.loads(reader.read())
        except FileNotFoundError:
            self._settings = {}


class Coordinates:
    _settings = {}

    def __init__(self, settings):
        self._settings = settings.get('Coordinates', {})

    @property
    def latitude(self):
        return self._settings.get('latitude', 41.621191)

    @property
    def longitude(self):
        return self._settings.get('longitude', -93.831609)