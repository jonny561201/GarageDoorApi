import json

from svc.utilities import gpio_utils
from svc.utilities import schedule_utils


def update_door_worker(ch, method, properties, body: bytes):
    try:
        request = json.loads(body)
        garage_id = request.get('id')
        action = request.get('action')

        if action == 'toggle':
            gpio_utils.toggle_garage_door(garage_id)
        elif action == 'update':
            gpio_utils.set_garage_door(garage_id, request['open'])
        elif action == 'schedule':
            schedule_utils.schedule_close(garage_id, request)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
