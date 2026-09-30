# Networking Module

Reusable networking foundation for application teams.

## Responsibilities

- Create an application VPC.
- Enable DNS support.
- Provide a private subnet.
- Apply standardized project and environment tags.

## Inputs

- `project_name`
- `environment`
- `vpc_cidr`

## Outputs

- `vpc_id`
- `private_subnet_id`

## Security

The module does not create public internet-facing resources by default.