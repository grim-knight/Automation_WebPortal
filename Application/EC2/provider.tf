terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0" # change based on the requirement
    }
  }
}

provider "aws" {
  region = "" # Add the region where the resources must be deployed
}