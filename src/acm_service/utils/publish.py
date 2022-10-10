import pika
from .env import CLOUDAMQP_URL
import json


class RabbitPublisher:

    def __init__(self) -> None:
        self.connection = None
        self.channel = None

    def publish(self, method, body) -> None:
        if self.connection is None:
            params = pika.URLParameters(CLOUDAMQP_URL)
            self.connection = pika.BlockingConnection(params)

        if self.channel is None:
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='main', durable=True)

        self.channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body),
                                   properties=pika.BasicProperties(
                                       delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                                       content_type=method))
        print('Publishing event :' + json.dumps(body))

    def __del__(self) -> None:
        if self.connection:
            self.connection.close()
