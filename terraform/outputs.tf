output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.budgetflow_server.id
}

output "public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.budgetflow_server.public_ip
}

output "public_dns" {
  description = "Public DNS of the EC2 instance"
  value       = aws_instance.budgetflow_server.public_dns
}

output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh -i budgetflow-key.pem ubuntu@${aws_instance.budgetflow_server.public_ip}"
}