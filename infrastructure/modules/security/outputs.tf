output "security_group_id" {
  description = "Application security group ID."
  value       = aws_security_group.application.id
}