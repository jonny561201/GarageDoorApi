from flask import Flask

from svc.routes.garage_door_routes import GARAGE_BLUEPRINT


app = Flask(__name__)
app.register_blueprint(GARAGE_BLUEPRINT)

