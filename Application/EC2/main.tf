locals { # this use case of locals helps you assign same tags for multiple instances being deployed simultaneously, change these tags based on requirements
  instance_tags = {
    OSVersion = "Amazon Linux 2023"
    AssetType = "CI-CD"
  }
}
module "ec2-instance" {
  source                 = "terraform-aws-modules/ec2-instance/aws"
  version                = "5.2.0"
  count                  = length(var.instance_name)
  ami                    = lookup(var.confvars, "amiid")
  instance_type          = lookup(var.confvars, "itype")
  subnet_id              = var.subnetsid[count.index]
  private_ip             = var.ip_address[count.index]
  iam_instance_profile   = lookup(var.confvars, "iam_profile")
  vpc_security_group_ids = [lookup(var.confvars, "secgroupid")] # use this line to configure a single security group
  # Line 19 must be used incase of configuring a secondary security group without conditional requirements
  # vpc_security_group_ids =[var.secgrp_2,lookup(var.confvars, "secgroupid")] # use this line if you want to assign multiple security groups
  # vpc_security_group_ids = count.index < 8 ? [var.secgrp_2,lookup(var.confvars, "secgroupid")] : [var.secgrp_3,lookup(var.confvars, "secgroupid")] # Uncomment and modify this line if you want to add secondary security group based on condition to different instances/VMs
  key_name = "" # Add the key-pair name to be associated with EC2 instances
  # launch_template = { #Uncomment this block if you want to provide a launch template
  #   id      = lookup(var.confvars, "launch_template")
  #   version = "$Latest"
  # }
  user_data = count.index < 1 ? file("master_jenkins.sh") : file("slave_jenkins.sh")# Uncomment this line if you want to pass any OS based commands (bash or powershell) Create a file and update the name of the same instead of userdata.ps1. (FYI - This is a startup script)
  tags = merge(
    {
      "Name"       = var.instance_name[count.index]
      "AssignedIP" = var.ip_address[count.index]
    },
    local.instance_tags
  )
  volume_tags = merge(
    {
      "Name"       = var.instance_name[count.index]
      "AssignedIP" = var.ip_address[count.index]
    },
    local.instance_tags
  )
}
