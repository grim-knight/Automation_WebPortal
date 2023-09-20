import jenkins

class JenkinsClient:
    def __init__(self, url, username, password):
        # Initialize JenkinsClient with the server URL, username, and password
        self.server = jenkins.Jenkins(url, username=username, password=password)

    def is_valid_credentials(self, username, token):
        # Check if the provided Jenkins credentials (username and token) are valid.
        # Return True if valid, False otherwise.
        try:
            # Attempt to make an API call to Jenkins using the provided credentials
            self.server.get_whoami()
            return True
        except jenkins.JenkinsException as e:
            # Handle any errors that occur during the API call
            print(f"Invalid Jenkins credentials: {str(e)}")
            return False
    
    def build_job(self, job_name, parameters=None):
        # Build a Jenkins job with optional parameters.
        # job_name: The name of the Jenkins job to build.
        # parameters: A dictionary of parameters to pass to the job (default is None).
        try:
            self.server.build_job(job_name, parameters)
            #  True if the job was successfully triggered, False otherwise.
            return True
        except Exception as e:
            # Handle and log any errors
            print(f"Error building Jenkins job: {str(e)}")
            return False

    def get_whoami(self):
        # Get information about the currently authenticated Jenkins user.
        # Information about the currently authenticated user.
        return self.server.get_whoami()
