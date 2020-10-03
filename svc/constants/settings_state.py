import json


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

    @staticmethod
    def get_instance():
        if Settings.__instance is None:
            Settings.__instance = Settings()
        return Settings.__instance

    def __get_settings(self):
        try:
            with open("./settings.json", "r") as reader:
                self.settings = json.loads(reader.read())
                self.dev_mode = self.settings.get("Development", False)
        except FileNotFoundError:
            self.settings = {}
