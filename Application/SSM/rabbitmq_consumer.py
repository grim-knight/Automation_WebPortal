import pika

def validate_and_establish_connection(hostname, port, username, password, virtual_host):
    """
    Validate RabbitMQ credentials and establish a connection.

    Args:
        hostname (str): RabbitMQ server hostname or IP address.
        port (int): RabbitMQ server port.
        username (str): RabbitMQ username.
        password (str): RabbitMQ password.
        virtual_host (str): RabbitMQ virtual host.

    Returns:
        pika.BlockingConnection: RabbitMQ connection object.
    """
    try:
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=hostname, port=port, credentials=credentials, virtual_host=virtual_host)
        connection = pika.BlockingConnection(parameters)
        return connection
    except pika.exceptions.AMQPError as e:
        print(f"Error: Unable to establish RabbitMQ connection: {str(e)}")
        return None

def consume_messages(connection, queue_name, callback):
    """
    Consume messages from a RabbitMQ queue.

    Args:
        connection (pika.BlockingConnection): RabbitMQ connection object.
        queue_name (str): Name of the queue to consume messages from.
        callback (function): Callback function to handle incoming messages.
    """
    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable = True, arguments={"x-message-ttl": 60000, "x-overflow": "reject-publish"})
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f'Waiting for messages in queue "{queue_name}". To exit, press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.AMQPError as e:
        print(f"Error: Unable to consume messages from RabbitMQ queue: {str(e)}")

# Example usage:
if __name__ == "__main__":
    rabbitmq_hostname = "localhost"  # Replace with your RabbitMQ server hostname or IP address
    rabbitmq_port = 5672            # Default RabbitMQ port
    rabbitmq_username = "svc_automation"
    rabbitmq_password = "1234"
    rabbitmq_virtual_host = "ssm_patch_automation"
    queue_name = "ssm_patch_automation_exchange_confirmation"           # Replace with your queue name

    connection = validate_and_establish_connection(rabbitmq_hostname, rabbitmq_port, rabbitmq_username, rabbitmq_password, rabbitmq_virtual_host)

    if connection:
        def message_callback(ch, method, properties, body):
            print(f"Received message: {body}")

        consume_messages(connection, queue_name, message_callback)
