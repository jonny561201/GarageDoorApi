import threading

from werkzeug.exceptions import BadRequest

from svc.config.sessions import Session
from svc.utilities import gpio_utils


def schedule_close(garage_id, request):
    try:
        delay_seconds = float(request['delay_seconds'])
    except KeyError:
        raise BadRequest

    session = Session.get_instance()

    def fire():
        session.clear_timer(garage_id)
        gpio_utils.set_garage_door(garage_id, False)

    timer = threading.Timer(delay_seconds, fire)
    timer.daemon = True
    session.set_timer(garage_id, timer)
    timer.start()


def cancel(garage_id):
    return Session.get_instance().clear_timer(garage_id)
