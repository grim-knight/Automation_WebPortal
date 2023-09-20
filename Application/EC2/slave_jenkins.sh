#!/bin/bash
sudo yum update -y
#Install java
sudo yum install java -y
#setup jenkins repo
sudo yum install jq -y
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum install jenkins -y
#Start jenkins service
sudo service jenkins start
# Enable the Jenkins service to start at boot with the command
sudo systemctl enable jenkins