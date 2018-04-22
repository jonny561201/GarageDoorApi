#!/Users/jonathongraf/.pyenv/versions/garage_door_env/bin/python
from flask import Flask
from flask import Response

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/garageDoor/status', methods=['GET'])
def garage_door_status():
    return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True)
