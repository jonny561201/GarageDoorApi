import json
from datetime import datetime

import pytz

from svc.config.settings_state import Settings


def get_door_duration(garage_id):
    file_name = Settings.get_instance().file_name
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = json.load(file)
            garage_date = content[garage_id]
            return datetime.fromisoformat(garage_date)
    except (FileNotFoundError, TypeError):
        now = datetime.now(tz=pytz.utc)
        content = {'1': now.isoformat(), '2': now.isoformat()}
        with open(file_name, "w+") as file:
            json.dump(content, file)
        return now
