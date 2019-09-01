import os
from datetime import timedelta, datetime

import jwt
import pytz
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from werkzeug.exceptions import Unauthorized


def is_jwt_valid(jwt_token):
    if jwt_token is None:
        raise Unauthorized
    _parse_jwt_token(jwt_token)


def create_jwt_token(user_id):
    expire_time = datetime.now(tz=pytz.timezone('US/Central')) + timedelta(hours=2)
    jwt_secret = os.environ['JWT_SECRET']
    return jwt.encode({'user_id': user_id, 'exp': expire_time}, jwt_secret, algorithm='HS256')


def _parse_jwt_token(jwt_token):
    try:
        stripped_token = jwt_token.replace('Bearer ', '')
        secret = os.environ['JWT_SECRET']
        jwt.decode(stripped_token, secret, algorithms=["HS256"])
    except (InvalidSignatureError, ExpiredSignatureError, DecodeError, KeyError) as er:
        raise Unauthorized
