import logging
from functools import partial

import pika

from svc.config.settings_state import Settings
from svc.constants.home_automation import Garage
from svc.utilities.event_client import MyThread


class RabbitMQClient:

    def __init__(self, settings: Settings):
        self.settings = settings.Queue
        self._connection = None
        self._channel = None

    def start_consumer(self, worker_function):
        t = MyThread.get_instance()
        bound_worker = partial(self._consume, worker_function)
        t.initialize(bound_worker)
        t.start()

    def _open_connection(self):
        credentials = pika.PlainCredentials(self.settings.user_name, self.settings.password)
        params = pika.ConnectionParameters(host=self.settings.host, port=self.settings.port, virtual_host=self.settings.vhost, credentials=credentials, socket_timeout=2)
        return pika.BlockingConnection(params)

    def _consume(self, worker_function):
        thread = MyThread.get_instance()
        while not thread.stopped.is_set():
            try:
                self._connection = self._open_connection()
                self._channel = self._connection.channel()
                self._channel.queue_declare(queue=Garage.QUEUE, durable=True)
                self._channel.basic_consume(queue=Garage.QUEUE, on_message_callback=worker_function, auto_ack=False)
                self._channel.start_consuming()
            except Exception:
                logging.exception('Queue consumer disconnected')
            finally:
                if self._connection is not None and self._connection.is_open:
                    self._connection.close()
                self._connection = None
                self._channel = None
            thread.stopped.wait(Garage.RECONNECT_SECONDS)
