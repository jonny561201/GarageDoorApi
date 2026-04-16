import json
from datetime import datetime
from zoneinfo import ZoneInfo

from svc.config.settings_state import Settings


def get_api_key():
    file_name = Settings.get_instance().api_key_file
    try:
        with open(file_name, 'r+', encoding='utf-8') as file:
            content = json.load(file)
        return content['api_key']
    except FileNotFoundError:
        return None


def save_api_key(api_key):
    file_name = Settings.get_instance().api_key_file
    with open(file_name, 'w+', encoding='utf-8') as file:
        content = {'api_key': api_key}
        json.dump(content, file)


def get_door_duration(garage_id: str):
    file_name = Settings.get_instance().garage_file
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = json.load(file)
            garage_date = content[garage_id]
            return datetime.fromisoformat(garage_date)
    except FileNotFoundError:
        return __create_file_if_not_exist(file_name)


def update_door_duration(garage_id: str):
    file_name = Settings.get_instance().garage_file
    try:
        with open(file_name, 'r+', encoding='utf-8') as file:
            content = json.load(file)
            content[garage_id] = datetime.now(tz=ZoneInfo('US/Central')).isoformat()
            file.seek(0)
            json.dump(content, file)
            file.truncate()
    except FileNotFoundError:
        __create_file_if_not_exist(file_name)


def __create_file_if_not_exist(file_name):
    now = datetime.now(tz=ZoneInfo('US/Central'))
    content = {'1': now.isoformat(), '2': now.isoformat()}
    with open(file_name, "w+") as file:
        json.dump(content, file)
    return now
