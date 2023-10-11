"""
Once your on-prem servers have installed the SSM agent and upon successful registration
Please make sure to validate the additions in the AWS Systems Manager Fleet Manager
Upon confirmation run this script to add name tags for those VM's and also to add the PatchGroup tags for those VM's
Make you update the value - default_patch_group
I would suggest you perform this functioned after you add the servers related to each environment (Stage, infra, prod)
In that way we can have unique tags for each environment and while patch patching those servers you won't patch prod servers which is no-go
"""

import subprocess
import json
import logging
import boto3

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize the AWS SSM client
ssm_client = boto3.client('ssm')

# Run the AWS CLI command to describe instance information and capture the output
command = [
    'aws', 'ssm', 'describe-instance-information',
    '--query', 'InstanceInformationList[].{InstanceId: InstanceId, IPAddress: IPAddress, ComputerName: ComputerName, PatchGroup: PatchGroup}',
    '--output', 'json'
]

# Specify the JSON output file name
output_file = 'instance_information.json'

try:
    # Run the AWS CLI command and capture the output to the JSON file
    with open(output_file, 'w') as json_file:
        result = subprocess.run(command, stdout=json_file, text=True, check=True)

    # Load the JSON data from the file
    with open(output_file, 'r') as json_file:
        instance_data = json.load(json_file)
except subprocess.CalledProcessError as e:
    logging.error(f"Error executing AWS CLI command: {e}")
    exit(1)
except json.JSONDecodeError as e:
    logging.error(f"Error decoding JSON response: {e}")
    exit(1)

# Filter instances with instance IDs starting with 'mi'
filtered_instances = [instance for instance in instance_data if instance['InstanceId'].startswith('mi')]

# Process the filtered instances and apply tags
for instance in filtered_instances:
    instance_id = instance['InstanceId']
    computer_name = instance['ComputerName']

    if computer_name is None:
        # Handle the case where the 'ComputerName' field is None
        logging.warning(f"Computer name is None for instance ID {instance_id}. Skipping...")
        continue  # Move to the next iteration/instance

    # Split the 'ComputerName' to extract the first part
    computer_name_parts = computer_name.split('.')
    if computer_name_parts:
        computer_name = computer_name_parts[0]

    # Check if the "Name" tag already exists for the instance
    tags = ssm_client.list_tags_for_resource(
        ResourceType='ManagedInstance',
        ResourceId=instance_id
    )['TagList']

    name_tag_exists = any(tag['Key'] == 'Name' for tag in tags)

    if not name_tag_exists:
        # Apply the "Name" tag to the instance using the extracted computer name
        ssm_client.add_tags_to_resource(
            ResourceType='ManagedInstance',
            ResourceId=instance_id,
            Tags=[{'Key': 'Name', 'Value': computer_name}]
        )

        logging.info(f"Created 'Name' tag for instance ID {instance_id} with value {computer_name}")

    # Check if the "PatchGroup" tag already exists for the instance
    patch_group_tag = next((tag for tag in tags if tag['Key'] == 'PatchGroup'), None)

    if patch_group_tag is None:
        # Create the "PatchGroup" tag with a default value if it doesn't exist
        default_patch_group = 'DefaultPatchGroup'  # You can change this value as needed
        ssm_client.add_tags_to_resource(
            ResourceType='ManagedInstance',
            ResourceId=instance_id,
            Tags=[{'Key': 'PatchGroup', 'Value': default_patch_group}]
        )

        logging.info(f"Created 'PatchGroup' tag for instance ID {instance_id}, Name: {computer_name} with value {default_patch_group}")
    else:
        logging.info(f"'PatchGroup' tag already exists for instance ID {instance_id}, Name: {computer_name} with value {patch_group_tag['Value']}")

print(f"Output saved to {output_file}")
