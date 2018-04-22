#!/Users/jonathongraf/.pyenv/versions/garage_door_env/bin/python
from flask import Flask, json
from flask import Response

app = Flask(__name__)

DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/garageDoor/status', methods=['GET'])
def garage_door_status():
    body = json.dumps({'garageStatus': True})
    return Response(body, status=200, headers=DEFAULT_HEADERS)


if __name__ == '__main__':
    app.run(debug=True)
