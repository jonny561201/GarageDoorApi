import os

import jwt
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from werkzeug.exceptions import Unauthorized

from svc.constants.settings_state import Settings


def is_jwt_valid(jwt_token):
    if jwt_token is None:
        raise Unauthorized
    _parse_jwt_token(jwt_token)


def _parse_jwt_token(jwt_token):
    try:
        stripped_token = jwt_token.replace('Bearer ', '')
        settings = Settings.get_instance().get_settings()
        if settings.get('Development'):
            return
        jwt.decode(stripped_token, os.environ['JWT_SECRET'], algorithms=["HS256"])
    except (InvalidSignatureError, ExpiredSignatureError, DecodeError, KeyError) as er:
        raise Unauthorized
