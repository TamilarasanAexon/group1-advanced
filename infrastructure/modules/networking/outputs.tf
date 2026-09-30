output "vpc_id" {
  description = "VPC identifier."
  value       = aws_vpc.this.id
}

output "private_subnet_id" {
  description = "Private subnet identifier."
  value       = aws_subnet.private.id
}