output "vpc_id" {
  description = "ID of the created VPC."
  value       = aws_vpc.this.id
}

output "private_subnet_id" {
  description = "ID of the private subnet."
  value       = aws_subnet.private.id
}

output "availability_zone_names" {
  description = "Selected Availability Zone names."
  value       = data.aws_availability_zones.available.names
}

output "vpc_flow_log_id" {
  description = "ID of the VPC flow log."
  value       = aws_flow_log.this.id
}