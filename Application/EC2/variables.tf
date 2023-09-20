variable "instance_name" {
  type    = list(any) # add the list of server names in the default
  default = []
}

variable "ip_address" {
  type    = list(any)
  default = [] # Add the list of IP addresses inside the default that must be assigned to the EC2 instances
}

variable "subnetsid" {
  type    = list(any)
  default = []  # Add the list of subnets ids inside the default that must be assigned to the EC2 instances
}


variable "confvars" {
  type = map(any)
  default = {
    secgroupid = ""  # Add the security group id required
    amiid      = "ami-0911e88fb4687e06b" # Amazon Linux 2 #Add the AMI id
    itype      = "t3.medium"             # Add the intance type here
    # launch_template  = "" # if you have a luanch template ID available then add that and uncomment this line
    iam_profile = "" # Add the IAM SSM role name that must be attached to the EC2 isntances
  }
}

# Utilize the below lines, if you want to add a second security group to your ec2 instances
# variable "secgrp_2"{
#   type = string
#   default = ""
# }
# variable "secgrp_3"{
#   type = string
#   default = ""# 
# }