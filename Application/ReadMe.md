The code base allows you build run and deploy a self service portal.

Make sure you have satisfied the below pre-requisites
1. Deploy terraform ec2 instance codes (Folder - EC2)) to create your infra for jenkins master and slave servers
2. Check if you can ssh from your master to slave, this validation is critical for next step.
3. Now configure the slave agents - https://www.pluralsight.com/resources/blog/cloud/adding-a-jenkins-agent-node
4. Once your jenkins setup is finished ,ake sure you install the jenkins plugin - "Pipeline Utility Steps"
5. https://dev.to/metaverse/install-rabbitmq-on-amamzon-ec2-amazon-linux-2-3dpd


AWS Systems Manager Pre-req
1. Make sure that you have created hyrid activation in your desired AWS region.
2. Safe gaurd the keys you get after creating the hybrid activations, these will be necessary for registration of servers (outside AWS) with AWS Systems Manager.
3. Also make sure you populate these in the 'windows_ssm_agent_instalation_script.ps1'


Windows Pre-req for air-gapped environment
    For windows environment setup your own WSUS --> https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/plan/plan-your-wsus-deployment
    (Setting up WSUS will help you create air gapped environment and only apply approved patches by your org) 
    Here is a youtube tutorial --> https://www.youtube.com/watch?v=Yv0qjxdX5yw

    http://www.isolation.se/importing-hotfixes-and-drivers-directly-into-wsus/
    Patch Manager Plus - https://www.manageengine.com/patch-management/wsus-alternative.html


    We also want to install the SSM agent on all the servers, AWS (AWS AMI's comes with ssm agent), VMware, Azure, GCP
    Copy the 'windows_ssm_agent_instalation_script.ps1' to a shared directory where all the windows servers in scope can access this file.
    and run the 'windows_ssm_agent_installation_automation.ps1' from Jump/Bastion server, which has access to all the servers. This script will reduce your effort of manually RDPing into each VM and running the SSM agent installation script.

Install the following packages on your server where you want to run the web app
pip install jenkins
pip install python-jenkins Flask
Rabbit MQ - Download the RabbitMQ installer from the official website for Windows or MacOS: https://www.rabbitmq.com/download.html
pip install pika --> RabbitMQ client library for python
sudo yum install jq -y --> on jenkins servers



<---Deprecated--->
Before you start with the pipeline execution make sure you have started the RabbitMQ Server
    Windows: Start the RabbitMQ service from the Windows Services Manager.
    MacOS: brew services start rabbitmq

    Make sure you create a new user and virtual host and assign required permission to that user.
    Set permission
        Virtual Host: /
        Configure regexp: .*
        Write regexp: .*
        Read regexp: .*

Instead of rabbitmq, I have opted for AWS Simple Queue Service, to reduce the maintenace overhead of rabbitmq.

<--->


AWS SQS
    Configure a SQS in you AWS account and make sure the jenkins master or slave, the IAM users, can publish and consume messages from the queue, this step is critical and configure IAM based on your requirements. FYI, Best practice is to use a service IAM user

