variable "project_name" {
  description = "Project name used for resource names and tags."
  type        = string
}

variable "environment" {
  description = "Deployment environment."
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block assigned to the VPC."
  type        = string
}

variable "private_subnet_cidr" {
  description = "CIDR block assigned to the private subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone_names" {
  description = "Explicit allowlist of Availability Zone names."
  type        = list(string)

  default = [
    "ap-south-1a",
    "ap-south-1b"
  ]

  validation {
    condition     = length(var.availability_zone_names) > 0
    error_message = "At least one Availability Zone name must be provided."
  }
}