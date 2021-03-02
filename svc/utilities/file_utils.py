import json
from datetime import datetime

import pytz

from svc.constants.settings_state import Settings


def get_door_duration(garage_id):
    file_name = Settings.get_instance().file_name
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = json.load(file)
            return content[garage_id]
    except (FileNotFoundError, TypeError):
        now = datetime.now(pytz.utc)
        content = {'1': f'{now :%Y-%m-%d %H:%M:%S%z}', '2': f'{now :%Y-%m-%d %H:%M:%S%z}'}
        with open(file_name, "w+") as file:
            json.dump(content, file)
        return content[garage_id]
