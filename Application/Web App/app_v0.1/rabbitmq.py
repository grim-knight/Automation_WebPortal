# Import the RabbitMQ library
import pika

# Create a class for handling RabbitMQ functionality
class RabbitMQClient:
    def __init__(self, host, username, password):
        # Initialize RabbitMQ client with host, username, and password
        self.host = host
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = None
        self.channel = None

    # Establish a connection to RabbitMQ server
    def connect(self):
        try:
            # Create a blocking connection to the RabbitMQ server
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, credentials=self.credentials)
            )
            self.channel = self.connection.channel()
        except Exception as e:
            print(f"Error connecting to RabbitMQ: {str(e)}")

    # Publish a message to a specified exchange and routing key
    def publish_message(self, exchange, routing_key, message):
        try:
            # Basic publish method to send a message
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=message,
                properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2)
            )
        except Exception as e:
            print(f"Error publishing message: {str(e)}")

    # Consume messages from a specified queue with a callback function
    def consume_messages(self, queue, callback):
        try:
            # Declare the queue to consume messages
            self.channel.queue_declare(queue=queue)
            
            # Start consuming messages from the queue
            self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
            
            # Print a message indicating that the client is waiting for messages
            print("Waiting for messages. To exit, press CTRL+C")
            
            # Start the message consuming loop
            self.channel.start_consuming()
        except Exception as e:
            print(f"Error consuming messages: {str(e)}")
