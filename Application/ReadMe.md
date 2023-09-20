The code base allow you build run and deploy a self service portal.
Make sure you have satisfied the below pre-requisites
1. Deploy terraform ec2 instance codes to create your infra
2. Check if you can ssh from your master to slave, this validation is critical for next step.
3. Now configure the slave agents - https://www.pluralsight.com/resources/blog/cloud/adding-a-jenkins-agent-node
4. Once your jenkins setup is finished ,ake sure you install the jenkins plugin - "Pipeline Utility Steps"
5. https://dev.to/metaverse/install-rabbitmq-on-amamzon-ec2-amazon-linux-2-3dpd

Windows Pre-req
For windows environment setup your own WSUS --> https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/plan/plan-your-wsus-deployment
(Setting up WSUS will help you create air gapped environment and only apply approved patches by your org) Here is youtube tutorial --> https://www.youtube.com/watch?v=Yv0qjxdX5yw

http://www.isolation.se/importing-hotfixes-and-drivers-directly-into-wsus/
Patch Manager Plus - https://www.manageengine.com/patch-management/wsus-alternative.html


Install the following packages
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
--->

Instead of rabbitmq, I have opted for AWS Simple Queue Service, to reduce the maintenace overhead of rabbitmq.

Configure a SQS in you AWS account and make sure the jenkins master or slave, the IAM users, can publish and consume messages from the queue, this step is critical and configure based on your requirements.

