from mock import MagicMock, patch

from svc.constants.home_automation import Garage
from svc.utilities.rabbitmq_client import RabbitMQClient


@patch('svc.utilities.rabbitmq_client.MyThread')
@patch('svc.utilities.rabbitmq_client.pika')
class TestRabbitMQClientConsume:
    WORKER = MagicMock()

    def setup_method(self):
        self.CLIENT = RabbitMQClient(MagicMock())

    def __arrange(self, mock_thread, loops):
        mock_thread.get_instance.return_value.stopped.is_set.side_effect = [False] * loops + [True]

    def test_consume__should_declare_queue_before_consuming(self, mock_pika, mock_thread):
        self.__arrange(mock_thread, 1)
        channel = mock_pika.BlockingConnection.return_value.channel.return_value

        self.CLIENT._consume(self.WORKER)

        channel.queue_declare.assert_called_once_with(queue=Garage.QUEUE, durable=True)
        channel.basic_consume.assert_called_once_with(queue=Garage.QUEUE, on_message_callback=self.WORKER, auto_ack=False)
        channel.start_consuming.assert_called_once()

    def test_consume__should_retry_after_broker_unavailable(self, mock_pika, mock_thread):
        self.__arrange(mock_thread, 2)
        mock_pika.BlockingConnection.side_effect = [Exception('refused'), MagicMock()]

        self.CLIENT._consume(self.WORKER)

        assert mock_pika.BlockingConnection.call_count == 2

    def test_consume__should_wait_between_reconnect_attempts(self, mock_pika, mock_thread):
        self.__arrange(mock_thread, 1)
        mock_pika.BlockingConnection.side_effect = Exception('refused')

        self.CLIENT._consume(self.WORKER)

        mock_thread.get_instance.return_value.stopped.wait.assert_called_once_with(Garage.RECONNECT_SECONDS)

    def test_consume__should_close_open_connection_after_consuming_stops(self, mock_pika, mock_thread):
        self.__arrange(mock_thread, 1)
        connection = mock_pika.BlockingConnection.return_value
        connection.is_open = True

        self.CLIENT._consume(self.WORKER)

        connection.close.assert_called_once()

    def test_consume__should_not_connect_when_already_stopped(self, mock_pika, mock_thread):
        self.__arrange(mock_thread, 0)

        self.CLIENT._consume(self.WORKER)

        mock_pika.BlockingConnection.assert_not_called()
