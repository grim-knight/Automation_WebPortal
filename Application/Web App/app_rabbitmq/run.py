from flask import Flask
from jenkins_app import JenkinsApp
from rabbitmq_client import RabbitMQClient
from jenkins_client import JenkinsClient
from rabbitmq_publisher import RabbitMQPublisher

app = Flask(__name__)

# RabbitMQ credentials
rabbitmq_host = "localhost"
rabbitmq_username = "svc_automation"
rabbitmq_password = "1234"
rabbitmq_virtual_host = "ssm_patch_automation"

# Jenkins credentials
jenkins_url = 'http://18.188.2.254:8080/'
jenkins_username = 'admin'
jenkins_password = '1234'

# Initialize classes
jenkins_client = JenkinsClient(jenkins_url, jenkins_username, jenkins_password)
rabbitmq_client = RabbitMQClient(rabbitmq_host, rabbitmq_username, rabbitmq_password, rabbitmq_virtual_host)
rabbitmq_client.connect()
rabbitmq_publisher = RabbitMQPublisher(rabbitmq_client)

if __name__ == '__main__':
    app_instance = JenkinsApp(jenkins_client, rabbitmq_client, rabbitmq_publisher)
    app_instance.run()