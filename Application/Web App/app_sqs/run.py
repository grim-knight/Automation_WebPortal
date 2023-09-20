from flask import Flask
from jenkins_app import JenkinsApp
from jenkins_client import JenkinsClient


app = Flask(__name__)

# Jenkins credentials
jenkins_url = 'http://18.188.2.254:8080/'
jenkins_username = 'admin'
jenkins_password = '1234'

# Initialize classes
jenkins_client = JenkinsClient(jenkins_url, jenkins_username, jenkins_password)

if __name__ == '__main__':
    app_instance = JenkinsApp(jenkins_client)
    app_instance.run()