# Terraform Modules Specification

## 1. Purpose

Provide reusable Infrastructure as Code modules that eliminate duplicated Terraform implementations across application teams.

## 2. Module Design

Each module must have:

```text
modules/<module-name>/
├── main.tf
├── variables.tf
├── outputs.tf
└── README.md
```

Modules must be composable rather than large application-specific stacks.

## 3. Module Contract

Every input must include:
- Name.
- Type.
- Description.
- Safe default where appropriate.
- Validation when a restricted value set is required.

Every output must:
- Have a stable name.
- Document what it represents.
- Avoid exposing secrets.

## 4. Security Requirements

- Never hard-code credentials.
- Never commit `.tfvars` files containing secrets.
- Use least-privilege IAM when cloud resources are added.
- Encrypt supported data stores using managed encryption facilities.
- Avoid publicly exposed resources unless explicitly required.
- Keep security configuration in reusable modules rather than relying on manual console configuration.

## 5. State Management

Production Terraform state should use an approved remote backend with access control and state locking where supported. The capstone baseline must remain locally validateable without requiring a remote backend.

## 6. Validation

Required commands:

```bash
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
```

Checkov must scan infrastructure during CI.

## 7. Versioning

Reusable modules should use explicit versions when consumed by application repositories. Breaking interface changes require a version change and migration documentation.

## 8. Acceptance Criteria

A module is accepted when:
- Its interface is documented.
- It passes formatting and validation.
- Checkov findings are reviewed.
- It can be consumed without copying its implementation.
- No credentials are embedded.
- The module has a clear ownership boundary.

## 9. Future Extension

The baseline module can be extended with standardized networking, IAM, container runtime and observability modules. Such additions must remain composable and independently testable.
