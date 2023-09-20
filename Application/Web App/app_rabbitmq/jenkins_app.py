from crypt import methods
from operator import methodcaller
from tkinter import Menubutton
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
import subprocess
import json
import pika
from jenkins_client import JenkinsClient  # Import JenkinsClient
from rabbitmq_client import RabbitMQClient  # Import RabbitMQClient
from rabbitmq_publisher import RabbitMQPublisher

class JenkinsApp:
    def __init__(self, jenkins_client, rabbitmq_client, rabbitmq_publisher):
        self.app = Flask(__name__)
        self.app.debug  = True
        self.app.secret_key = 'automate'  # Set your secret key here
        self.jenkins_client = jenkins_client  # Store JenkinsClient instance
        self.rabbitmq_client = rabbitmq_client  # Store RabbitMQClient instance
        self.rabbitmq_publisher = rabbitmq_publisher

        # Define routes
        self.app.route('/')(self.landing)  # Landing page
        self.app.route('/pipeline')(self.pipeline_page)  # Pipeline page
        self.app.route('/trigger-pipeline', methods=['POST'])(self.trigger_pipeline)  # Trigger selected pipeline
        self.app.route('/confirm-instance-info', methods=['POST'])(self.confirm_instance_info)  # Confirm instance information
        self.app.route('/flash_messages', methods=['GET'])(self.flash_messages)  # Confirm instance information

    def run(self):
        self.app.run(host='127.0.0.1', port=5000)

    def landing(self):
        return render_template('landing.html')

    def pipeline_page(self):
        return render_template('pipeline.html')
    
    def flash_messages(self):
        return render_template('flash_messages.html')

    def trigger_pipeline(self):
        try:
            # Verify Jenkins credentials by making an API call
            username = request.form.get('username')
            token = request.form.get('token')

            if self.jenkins_client.is_valid_credentials(username, token):  # Use the JenkinsClient isvalidcredentials method
                # Get the selected pipeline option from the form
                selected_pipeline = request.form.get('pipeline_option')  # Use the same variable name
                print(f'Received pipeline: {selected_pipeline}')

                # Map the selected option to the corresponding Jenkins job name
                pipeline_job_mapping = {
                    # Replace with the actual jenkins job name and update the environments too. Example, Stage, infra and prod.
                    # make sure the environment name here matches the parameters declared in the jenkins pipeline script
                    'stage': 'ssm_patch_automation_env_specific',  
                }

                # Trigger the selected pipeline
                job_name = pipeline_job_mapping.get(selected_pipeline)
                print(f'Received job: {job_name}')

                # Retrieve the selected environment from the form
                selected_environment = request.form.get('pipeline_option')

                if job_name:
                    # Modify the parameters dictionary to include the selected environment
                    parameters = {
                        'ENVIRONMENT': selected_environment,
                    }

                    self.jenkins_client.build_job(job_name, parameters)  # Use the JenkinsClient method

                    # Fetch AWS instance information and store it in a JSON file
                    aws_command = "aws ssm describe-instance-information --filter 'Key=tag-key,Values=PatchGroup' " \
                                "--query 'InstanceInformationList[].{InstanceId: InstanceId, IPAddress: IPAddress, " \
                                "ComputerName: ComputerName}' --output json"
                    try:
                        aws_output = subprocess.check_output(aws_command, shell=True, stderr=subprocess.STDOUT)
                        instance_info = json.loads(aws_output)
                        
                        # Save the instance information to a JSON file
                        with open('instance_info.json', 'w') as json_file:
                            json.dump(instance_info, json_file)
                        return render_template('confirm.html', instance_info=instance_info)
                    except subprocess.CalledProcessError as e:
                        # Handle any errors that occurred while running the AWS CLI command
                        print(f"Error executing AWS CLI command: {e}")

                else:
                    return jsonify({'message': 'Invalid pipeline option'}), 400  # Bad Request
            else:
                return jsonify({'message': 'Invalid Jenkins credentials'}), 403  # Forbidden
        except Exception as e:
            return jsonify({'message': f'Failed to trigger pipeline: {str(e)}'}), 500  # Failed to trigger

    def confirm_instance_info(self):
        try:
            # Check if the user confirmed the instance information
            user_message = request.form.get('message')
            print(user_message)
            if user_message == 'Proceed':
                # Publish the confirmation message to RabbitMQ
                self.rabbitmq_publisher.publish_message('ssm_patch_automation_exchange', 'ssm_patch_automation', user_message)

                # Proceed with the pipeline
                # Add your code here to continue with the Jenkins pipeline
                flash('Pipeline is proceeding...Message published in rabbitmq')
                return redirect(url_for('flash_messages'))
            else:
                self.rabbitmq_publisher.publish_message('ssm_patch_automation_exchange', 'ssm_patch_automation', user_message)
                flash('Pipeline is canceled by the user....Abort published')
                return redirect(url_for('flash_messages'))

        except Exception as e:
            return jsonify({'message': f'Failed to confirm instance info: {str(e)}'}), 500