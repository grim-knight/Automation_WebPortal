from rabbitmq_client import RabbitMQClient
import pika

class RabbitMQPublisher:
    def __init__(self, rabbitmq_client):
        self.rabbitmq_client = rabbitmq_client

    def publish_message(self, exchange, routing_key, message):
        # Validate credentials for rabbitmq
        if self.rabbitmq_client.connect():
            try:
                self.rabbitmq_client.channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=message,
                    properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2)
                )
                print(f"Message published: {message}")
            except Exception as e:
                # Handle and log any errors
                print(f"Error publishing message: {str(e)}")
        else:
            print("Invalid RabbitMQ credentials. Cannot publish message.")
