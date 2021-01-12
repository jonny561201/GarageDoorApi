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
        return f'{datetime.now(pytz.utc):%Y-%m-%d %H:%M:%S%z}'
