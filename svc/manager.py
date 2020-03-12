from flask import Flask
from flask_cors import CORS

from svc.routes.garage_door_routes import GARAGE_BLUEPRINT


def create_app(app_name):
    if app_name == '__main__':
        app = Flask(app_name)
        CORS(app)
        app.register_blueprint(GARAGE_BLUEPRINT)

        return app
