from flask import Flask
from jenkins_app import JenkinsApp
from jenkins_client import JenkinsClient
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Add log messages
logging.debug('Debug message')
logging.info('Info message')
logging.warning('Warning message')


app = Flask(__name__)

# Jenkins credentials
# Change the values based on your config
jenkins_url = 'http://18.117.106.39:8080/'
jenkins_username = 'admin'
jenkins_password = '1234'

# Initialize classes
jenkins_client = JenkinsClient(jenkins_url, jenkins_username, jenkins_password)

if __name__ == '__main__':
    app_instance = JenkinsApp(jenkins_client)
    app_instance.run()