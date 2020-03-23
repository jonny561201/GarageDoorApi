from flask import Flask

from svc.routes.garage_door_routes import GARAGE_BLUEPRINT


def create_app(app_name):
    if app_name == '__main__':
        app = Flask(app_name)
        app.register_blueprint(GARAGE_BLUEPRINT)

        return app
