#!/Users/jonathongraf/.pyenv/versions/garage_door_env/bin/python
import os

import jwt
from flask import Flask, json
from flask import Response
from flask import request

from db.user_credentials import UserDatabaseManager

app = Flask(__name__)

DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/garageDoor/login', methods=['POST'])
def garage_door_login():
    post_body = request.data
    with UserDatabaseManager() as user_database:
        if user_database.user_credentials_are_valid(post_body):
            jwt_secret = os.environ.get('JWT_SECRET')
            jwt_token = jwt.encode({'user_id': 12345}, jwt_secret, algorithm='HS256')
            return Response(jwt_token, status=200)
        else:
            return Response(status=401)


@app.route('/garageDoor/status', methods=['GET'])
def garage_door_status():
    body = json.dumps({'garageStatus': True})
    return Response(body, status=200, headers=DEFAULT_HEADERS)


@app.route('/garageDoor/state', methods=['POST'])
def update_garage_door_state():
    request_body = request.data
    return Response(json.dumps(request_body), status=200, headers=DEFAULT_HEADERS)


if __name__ == '__main__':
    app.run(debug=True)
