import os

import jwt
from jwt import InvalidSignatureError


def is_jwt_valid(jwt_token):
    try:
        decrypted_token = jwt.decode(jwt_token, os.environ['JWT_SECRET'], algorithms=["HS256"])
        return True
    except InvalidSignatureError as er:
        return False
