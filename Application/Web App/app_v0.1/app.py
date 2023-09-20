from flask import Flask, request, render_template, jsonify
import jenkins
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Add log messages
logging.debug('Debug message')
logging.info('Info message')
logging.warning('Warning message')


app = Flask(__name__)

# Jenkins server configuration
jenkins_url = 'http://3.143.255.53:8080'  # Replace with your Jenkins server URL
jenkins_username = 'admin'  # Replace with your Jenkins username
jenkins_password = '1234'  # Replace with your Jenkins password or API token

# Create a Jenkins server connection
jenkins_server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trigger-pipeline', methods=['POST'])
def trigger_pipeline():
    try:
        # Verify Jenkins credentials by making an API call
        username = request.form.get('username')
        token = request.form.get('token')
        print(jenkins_server.get_whoami()['fullName'])

        if jenkins_server.get_whoami()['fullName'] == username:
            # Trigger the Jenkins pipeline
            job_name = 'ssm_patch_automation'  # Replace with your Jenkins job name
            jenkins_server.build_job(job_name)
            return jsonify({'message': 'Jenkins pipeline triggered successfully'}), 200 # Success
        else:
            return jsonify({'message': 'Invalid Jenkins credentials'}), 403  # Forbidden
    except Exception as e:
        return jsonify({'message': f'Failed to trigger Jenkins pipeline: {str(e)}'}), 500 # Failed to trigger

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
