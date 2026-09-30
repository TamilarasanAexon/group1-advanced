output "application_name" {
  description = "Application identifier."
  value       = "${var.project_name}-${var.environment}"
}