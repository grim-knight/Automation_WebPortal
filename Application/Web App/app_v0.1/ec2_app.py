import subprocess
import json

# Execute the AWS CLI command and capture its output
aws_command = "aws ssm describe-instance-information --filter 'Key=tag-key,Values=PatchGroup' --query 'InstanceInformationList[].{InstanceId: InstanceId, IPAddress: IPAddress, ComputerName: ComputerName}' --output json"
try:
    aws_output = subprocess.check_output(aws_command, shell=True, stderr=subprocess.STDOUT)
    instance_info = json.loads(aws_output)
    
    # Save the instance information to a JSON file
    with open('instance_info.json', 'w') as json_file:
        json.dump(instance_info, json_file)
    
    # Continue with the rest of your code, including displaying the instance information
    # in the HTML template and prompting the user for confirmation.
except subprocess.CalledProcessError as e:
    # Handle any errors that occurred while running the AWS CLI command
    print(f"Error executing AWS CLI command: {e}")