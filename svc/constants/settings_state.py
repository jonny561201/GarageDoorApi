import json
import os


class Settings:
    __instance = None
    settings = None
    dev_mode = False

    def __init__(self):
        if Settings.__instance is not None:
            raise Exception
        else:
            Settings.__instance = self
            Settings.__instance.__get_settings()

    @property
    def jwt_secret(self):
        return self.settings.get('DevJwtSecret') if self.dev_mode else os.environ.get('JWT_SECRET')

    @property
    def file_name(self):
        return self.settings.get('FileName') if self.dev_mode else os.environ.get('FILE_NAME', 'garageStatus.json')

    @property
    def dev_coordinates(self):
        return self.settings.get('DevCoordinates') if self.dev_mode else {'latitude': 41.621191, 'longitude': -93.831609}

    @staticmethod
    def get_instance():
        if Settings.__instance is None:
            Settings.__instance = Settings()
        return Settings.__instance

    def __get_settings(self):
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.json')
            with open(file_path, "r") as reader:
                self.settings = json.loads(reader.read())
                self.dev_mode = self.settings.get("Development", False)
        except FileNotFoundError:
            self.settings = {}
