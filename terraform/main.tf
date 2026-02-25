terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ─── KEY PAIR ───────────────────────────────────────────
resource "aws_key_pair" "budgetflow_key" {
  key_name   = var.key_name
  public_key = file("${path.module}/budgetflow-key.pub")
}

# ─── SECURITY GROUP ─────────────────────────────────────
resource "aws_security_group" "budgetflow_sg" {
  name        = "${var.app_name}-sg"
  description = "Security group for BudgetFlow app"

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Flask (direct access)
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound - allow all
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.app_name}-sg"
  }
}

# ─── EC2 INSTANCE ────────────────────────────────────────
resource "aws_instance" "budgetflow_server" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.budgetflow_key.key_name
  vpc_security_group_ids = [aws_security_group.budgetflow_sg.id]

  tags = {
    Name        = "${var.app_name}-server"
    Environment = "production"
    Project     = "budgetflow"
  }

  # Basic server setup on launch
  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y python3 python3-pip nginx git
  EOF
}