import secrets

from werkzeug.exceptions import Unauthorized

from svc.utilities.file_utils import get_api_key, save_api_key


def get_generate_api_key():
    existing_key = get_api_key()
    if existing_key:
        return existing_key
    api_key = secrets.token_hex(32)
    save_api_key(api_key)
    return api_key


def validate_api_key(api_key):
    valid_key = get_api_key()
    if valid_key is None or api_key != valid_key:
        raise Unauthorized()
