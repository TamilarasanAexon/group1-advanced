# Repository Template Specification

## 1. Purpose

Provide every application team with the same starting repository so that common engineering decisions do not have to be recreated for every project.

## 2. Required Structure

```text
README.md
app/
infrastructure/
.github/workflows/
docs/
architecture/
ai-specifications/
engineering-decisions/
presentation/
```

## 3. Standard Application Contract

An onboarded application must provide:
- Application source code under `app/`.
- A Dockerfile.
- A health endpoint.
- Automated tests.
- Infrastructure configuration under `infrastructure/`.
- CI workflow integration.
- Security scanning.
- Developer onboarding documentation.

## 4. Configuration Model

Application teams should configure:
- Application name.
- Environment names.
- Runtime-specific parameters.
- Business-specific test suites.
- Approved infrastructure module inputs.

Teams should not duplicate or independently rewrite common security and CI logic.

## 5. Template Quality Gates

The template must:
- Build locally.
- Pass tests.
- Pass Terraform validation.
- Execute security scans.
- Contain no committed secrets.
- Include onboarding documentation.
- Include ownership information.

## 6. Onboarding Flow

```text
Create repository
      ↓
Set application metadata
      ↓
Run local validation
      ↓
Open pull request
      ↓
Automated quality/security checks
      ↓
Code review
      ↓
Merge
      ↓
Release workflow
```

## 7. Acceptance Criteria

A second application must be able to adopt the template without copying implementation-specific code from IMS. Only application-specific source, configuration and approved module parameters should need to change.
