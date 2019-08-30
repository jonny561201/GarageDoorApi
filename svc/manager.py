from flask import Flask

from svc.routes.garage_door_routes import route_blueprint


def create_app(app_name):
    if app_name == '__main__':
        app = Flask(app_name)
        app.register_blueprint(route_blueprint)

        return app
