import pika

class RabbitMQClient:
    def __init__(self, host, username, password, virtual_host):
        # Initialize RabbitMQClient with host, username, and password
        self.host = host
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = None
        self.channel = None

    def connect(self):
        # Establish a connection to the RabbitMQ server with the virtual host.
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, credentials=self.credentials, virtual_host=self.virtual_host)
            )
            self.channel = self.connection.channel()
            print("Credential validation success")
            return True
        except Exception as e:
            # Handle and log any errors
            print(f"Error connecting to RabbitMQ: {str(e)}")