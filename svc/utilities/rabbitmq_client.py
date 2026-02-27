from functools import partial

import pika

from svc.config.settings_state import Settings
from svc.constants.home_automation import Automation
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

    def stop_consumer(self):
        if not self._connection or not self._channel:
            return

        try:
            self._connection.add_callback_threadsafe(lambda: self._channel.stop_consuming())
        except Exception:
            pass

        t = MyThread.get_instance()
        t.stop()
        try:
            t.join(5)
        except RuntimeError:
            pass

    def _open_connection(self):
        credentials = pika.PlainCredentials(self.settings.user_name, self.settings.password)
        params = pika.ConnectionParameters(host=self.settings.host, port=self.settings.port, virtual_host=self.settings.vhost, credentials=credentials, socket_timeout=2)
        return pika.BlockingConnection(params)

    def _consume(self, worker_function):
        try:
            self._connection = self._open_connection()
        except Exception as exc:
            raise Exception(f'Broker Unavailable: \n {str(exc)}')
        try:
            self._channel = self._connection.channel()
            self._channel.basic_consume(queue=Automation.GARAGE.QUEUE, on_message_callback=worker_function, auto_ack=False)
            self._channel.start_consuming()
        finally:
            self._connection.close() if self._connection else None
            self._connection = None
            self._channel = None



# thread = RabbitMQClient(Settings.get_instance())
# def sample(channel, method, properties, body):
#     print('Received message')
#     print(body)
#
# thread.start_consumer(sample)
# time.sleep(2)
# thread.stop_consumer()



