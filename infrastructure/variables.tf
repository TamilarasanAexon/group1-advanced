variable "project_name" {
  description = "Application or platform project name."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "project_name must contain only lowercase letters, numbers and hyphens."
  }
}

variable "environment" {
  description = "Deployment environment."
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging or prod."
  }
}

variable "aws_region" {
  description = "AWS region used by the deployment."
  type        = string
  default     = "ap-south-1"
}

variable "vpc_cidr" {
  description = "CIDR range for the application VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "enable_networking" {
  description = "Whether the reusable networking module should be enabled."
  type        = bool
  default     = true
}

variable "enable_security" {
  description = "Whether the reusable security baseline should be enabled."
  type        = bool
  default     = true
}