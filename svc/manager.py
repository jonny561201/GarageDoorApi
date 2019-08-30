from flask import Flask

from svc.routes.garage_door_routes import GARAGE_BLUEPRINT
from svc.routes.thermostat_routes import THERMOSTAT_BLUEPRINT


def create_app(app_name):
    if app_name == '__main__':
        app = Flask(app_name)
        app.register_blueprint(THERMOSTAT_BLUEPRINT)
        app.register_blueprint(GARAGE_BLUEPRINT)

        return app
