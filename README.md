# Acme Retail — AI-Driven Cloud & DevSecOps Platform

A reusable Internal Developer Platform foundation for Acme Retail application teams.

## Goals
- Standardize repository structure, CI/CD, security, IaC and documentation.
- Reduce duplicate Terraform and GitHub Actions.
- Provide reusable AI Engineering Specifications.
- Enable self-service onboarding with minimal customization.
- Remain reproducible locally without dedicated cloud infrastructure.

## Technology
Git/GitHub, GitHub Actions, Terraform, Docker, AWS (preferred target), Trivy, Checkov, Gitleaks, Markdown, Mermaid.

## Repository layout
```text
app/
infrastructure/
.github/workflows/
docs/architecture/
ai-specifications/
engineering-decisions/
presentation/
```

## Local validation
```bash
docker build -t acme-ims:local app
docker run --rm -p 8080:8080 acme-ims:local
terraform -chdir=infrastructure fmt -check -recursive
terraform -chdir=infrastructure validate
```

## Security
CI runs secret scanning, IaC scanning, container scanning and tests. Production credentials must never be committed.

## Capstone alignment
The participant guide requires reusable platform capabilities, six AI Engineering Specifications, IaC, CI/CD, architecture documentation, ADRs and a final presentation.


## Platform implementation status

The six AI Engineering Specifications define the target platform contract. Implementation changes should be evaluated against these specifications before being accepted.

### Validation checklist

- [ ] All six specifications reviewed.
- [ ] Application tests pass.
- [ ] Docker image builds.
- [ ] Terraform formatting passes.
- [ ] Terraform validation passes.
- [ ] Gitleaks passes.
- [ ] Checkov findings reviewed.
- [ ] Trivy findings reviewed.
- [ ] Architecture documentation matches implementation.
- [ ] ADRs capture significant decisions.
- [ ] Final presentation includes validation evidence.
