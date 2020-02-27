import json


class Settings:
    __instance = None
    settings = None

    def __init__(self):
        if Settings.__instance is not None:
            raise Exception
        else:
            Settings.__instance = self

    @staticmethod
    def get_instance():
        if Settings.__instance is None:
            Settings.__instance = Settings()
        return Settings.__instance

    def get_settings(self):
        if self.settings is None:
            try:
                with open("./settings.json", "r") as reader:
                    self.settings = json.loads(reader.read())
                return self.settings
            except FileNotFoundError:
                return {}
        else:
            return self.settings
