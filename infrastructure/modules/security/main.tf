data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "application" {
  name        = "${var.project_name}-${var.environment}-application"
  description = "Application security group"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Application traffic"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  egress {
    description = "Outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-application"
  }
}