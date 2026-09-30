locals {
  application_name = "${var.project_name}-${var.environment}"
}

output "application_name" {
  description = "Standardized application name."
  value       = local.application_name
}