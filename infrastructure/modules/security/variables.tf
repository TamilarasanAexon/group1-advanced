variable "project_name" {
  description = "Project name used for resource names and tags."
  type        = string
}

variable "environment" {
  description = "Deployment environment."
  type        = string
}

variable "vpc_id" {
  description = "VPC in which the security group is created."
  type        = string
}

variable "subnet_id" {
  description = "Subnet used by the application network interface."
  type        = string
}

variable "allowed_application_cidr" {
  description = "CIDR permitted to access application port 8080."
  type        = string
  default     = "10.0.0.0/8"
}