import os
from datetime import timedelta, datetime

import jwt
import pytz
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError

TEMP_SECRET = 'temporarySecret'


def is_jwt_valid(jwt_token):
    return False if jwt_token is None else _parse_jwt_token(jwt_token)


def create_jwt_token():
    expire_time = datetime.now(tz=pytz.timezone('US/Central')) + timedelta(hours=2)
    jwt_secret = os.environ.get('JWT_SECRET', TEMP_SECRET)
    return jwt.encode({'user_id': 12345, 'exp': expire_time}, jwt_secret, algorithm='HS256')


def _parse_jwt_token(jwt_token):
    try:
        stripped_token = jwt_token.replace('Bearer ', '')
        secret = os.environ.get('JWT_SECRET', TEMP_SECRET)
        jwt.decode(stripped_token, secret, algorithms=["HS256"])
        return True
    except (InvalidSignatureError, ExpiredSignatureError, DecodeError, KeyError) as er:
        return False
