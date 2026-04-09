from flask import Flask

from svc.config.settings_state import Settings
from svc.controllers.garage_door_controller import update_door_worker
from svc.endpoints.app_routes import APP_BLUEPRINT
from svc.endpoints.garage_door_routes import GARAGE_BLUEPRINT
from svc.utilities.mdns_registration import MdnsRegistration
from svc.utilities.rabbitmq_client import RabbitMQClient


app = Flask(__name__)
app.register_blueprint(GARAGE_BLUEPRINT)
app.register_blueprint(APP_BLUEPRINT)

mdns = MdnsRegistration(port=5001)
mdns.register()

client = RabbitMQClient(Settings.get_instance())
client.start_consumer(update_door_worker)