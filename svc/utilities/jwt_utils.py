import os
from datetime import timedelta, datetime

import jwt
import pytz
from jwt import ExpiredSignatureError
from jwt import InvalidSignatureError


def is_jwt_valid(jwt_token):
    try:
        decrypted_token = jwt.decode(jwt_token, os.environ['JWT_SECRET'], algorithms=["HS256"])
        return True
    except (InvalidSignatureError, ExpiredSignatureError) as er:
        return False


def create_jwt_token():
    expire_time = datetime.now(tz=pytz.timezone('US/Central')) + timedelta(hours=2)
    jwt_secret = os.environ.get('JWT_SECRET')
    return jwt.encode({'user_id': 12345, 'exp': expire_time}, jwt_secret, algorithm='HS256')
