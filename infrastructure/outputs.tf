output "project_name" {
  description = "Application project name."
  value       = var.project_name
}

output "environment" {
  description = "Deployment environment."
  value       = var.environment
}

output "vpc_id" {
  description = "VPC ID created by the networking module."
  value       = try(module.networking[0].vpc_id, null)
}

output "security_group_id" {
  description = "Application security group ID."
  value       = try(module.security[0].security_group_id, null)
}

output "application_name" {
  description = "Standardized application identifier."
  value       = module.application_baseline.application_name
}