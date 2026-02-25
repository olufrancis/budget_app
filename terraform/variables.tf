variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "eu-west-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "Ubuntu 22.04 LTS AMI ID"
  default     = "ami-0905a3c97561e0b69"  # Ubuntu 22.04 eu-west-1
}

variable "key_name" {
  description = "Name of the AWS key pair"
  default     = "budgetflow-key"
}

variable "app_name" {
  description = "Application name"
  default     = "budgetflow"
}