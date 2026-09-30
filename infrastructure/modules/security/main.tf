resource "aws_security_group" "application" {
  name        = "${var.project_name}-${var.environment}-application"
  description = "Application security group"
  vpc_id      = var.vpc_id

  ingress {
    description = "Application traffic from the approved CIDR"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = [var.allowed_application_cidr]
  }

  egress {
    description = "HTTPS outbound traffic"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-application"
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_network_interface" "application" {
  subnet_id       = var.subnet_id
  security_groups = [aws_security_group.application.id]
  description     = "Application network interface"

  tags = {
    Name        = "${var.project_name}-${var.environment}-application-eni"
    Project     = var.project_name
    Environment = var.environment
  }
}