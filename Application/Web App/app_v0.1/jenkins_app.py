# from flask import Flask, request, render_template, jsonify, redirect, url_for
# import jenkins
# import logging

# # # Configure logging
# # logging.basicConfig(filename='app.log', level=logging.DEBUG)

# # # Add log messages
# # logging.debug('Debug message')
# # logging.info('Info message')
# # logging.warning('Warning message')

# class JenkinsApp:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.app.debug  = True

#         # ... Jenkins server configuration ...
#         self.jenkins_url = 'http://3.143.255.53:8080'  # Replace with your Jenkins server URL
#         self.jenkins_username = 'admin'  # Replace with your Jenkins username
#         self.jenkins_password = '1234'  # Replace with your Jenkins password or API token

#         self.jenkins_server = jenkins.Jenkins(self.jenkins_url, username=self.jenkins_username, password=self.jenkins_password)

#         # Define routes
#         self.app.route('/')(self.landing)  # Landing page
#         self.app.route('/pipeline')(self.pipeline_page)  # Pipeline page
#         self.app.route('/trigger-pipeline', methods=['POST'])(self.trigger_pipeline)  # Trigger selected pipeline
#     def run(self):
#         self.app.run(host='127.0.0.1', port=5000)

#     def landing(self):
#         return render_template('landing.html')

#     def pipeline_page(self):
#         return render_template('pipeline.html')

#     def trigger_pipeline(self):
#         try:
#             # Verify Jenkins credentials by making an API call
#             username = request.form.get('username')
#             token = request.form.get('token')

#             if self.jenkins_server.get_whoami()['fullName'] == username:
#                 # Get the selected pipeline option from the form
#                 selected_pipeline = request.form.get('pipeline_option')  # Use the same variable name
#                 print(f'Received pipeline: {selected_pipeline}')

#                 # Map the selected option to the corresponding Jenkins job name
#                 pipeline_job_mapping = {
#                     'stage': 'ssm_patch_automation_env_specific',  # Replace with the actual job name for jenkins Pipeline
#                 }

#                 # Trigger the selected pipeline
#                 job_name = pipeline_job_mapping.get(selected_pipeline)
#                 print(f'Received job: {job_name}')

#                 # Retrieve the selected environment from the form
#                 selected_environment = request.form.get('pipeline_option')

#                 if job_name:
#                     # Modify the parameters dictionary to include the selected environment
#                     parameters = {
#                         'ENVIRONMENT': selected_environment,
#                     }

#                     self.jenkins_server.build_job(job_name, parameters)
#                     return jsonify({'message': f'{selected_pipeline} triggered successfully'}), 200  # Success
#                 else:
#                     return jsonify({'message': 'Invalid pipeline option'}), 400  # Bad Request
#             else:
#                 return jsonify({'message': 'Invalid Jenkins credentials'}), 403  # Forbidden
#         except Exception as e:
#             return jsonify({'message': f'Failed to trigger pipeline: {str(e)}'}), 500  # Failed to trigger


from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
import jenkins
import logging
import subprocess
import json

# # Configure logging
# logging.basicConfig(filename='app.log', level=logging.DEBUG)

# # Add log messages
# logging.debug('Debug message')
# logging.info('Info message')
# logging.warning('Warning message')

class JenkinsApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.debug  = True

        # ... Jenkins server configuration ...
        self.jenkins_url = 'http://3.143.255.53:8080'  # Replace with your Jenkins server URL
        self.jenkins_username = 'admin'  # Replace with your Jenkins username
        self.jenkins_password = '1234'  # Replace with your Jenkins password or API token

        self.jenkins_server = jenkins.Jenkins(self.jenkins_url, username=self.jenkins_username, password=self.jenkins_password)

        # Define routes
        self.app.route('/')(self.landing)  # Landing page
        self.app.route('/pipeline')(self.pipeline_page)  # Pipeline page
        self.app.route('/trigger-pipeline', methods=['POST'])(self.trigger_pipeline)  # Trigger selected pipeline
        self.app.route('/confirm-instance-info', methods=['POST'])(self.confirm_instance_info)  # Confirm instance information

    def run(self):
        self.app.run(host='127.0.0.1', port=5000)

    def landing(self):
        return render_template('landing.html')

    def pipeline_page(self):
        return render_template('pipeline.html')

    def trigger_pipeline(self):
        try:
            # Verify Jenkins credentials by making an API call
            username = request.form.get('username')
            token = request.form.get('token')

            if self.jenkins_server.get_whoami()['fullName'] == username:
                # Get the selected pipeline option from the form
                selected_pipeline = request.form.get('pipeline_option')  # Use the same variable name
                print(f'Received pipeline: {selected_pipeline}')

                # Map the selected option to the corresponding Jenkins job name
                pipeline_job_mapping = {
                    'stage': 'ssm_patch_automation_env_specific',  # Replace with the actual job name for Jenkins Pipeline
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

                    self.jenkins_server.build_job(job_name, parameters)

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
            user_confirmation = request.form.get('confirmation')

            if user_confirmation == 'Proceed':
                # Proceed with the pipeline
                # Add your code here to continue with the Jenkins pipeline
                flash('Pipeline is proceeding...')
                return redirect(url_for('pipeline_page'))

            else:
                flash('Pipeline is canceled by the user.')
                return redirect(url_for('landing'))

        except Exception as e:
            return jsonify({'message': f'Failed to confirm instance info: {str(e)}'}), 500