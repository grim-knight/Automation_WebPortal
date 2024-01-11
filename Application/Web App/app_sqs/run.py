from distutils.log import debug
from flask import Flask
from jenkins_app import JenkinsApp
from jenkins_client import JenkinsClient
from dashboard import Dashboard, dashboard_bp
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Add log messages
logging.debug('Debug message')
logging.info('Info message')
logging.warning('Warning message')

app = Flask(__name__)
app.register_blueprint(dashboard_bp)

# Jenkins credentials
# Change the values based on your config
jenkins_url = 'http://18.117.106.39:8080/'
jenkins_username = 'admin'
jenkins_password = '1234'

# Initialize classes
jenkins_client = JenkinsClient(jenkins_url, jenkins_username, jenkins_password)



if __name__ == '__main__':
    app = JenkinsApp(jenkins_client)
    app.run()