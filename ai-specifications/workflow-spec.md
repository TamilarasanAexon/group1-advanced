# GitHub Actions Workflow Specification

## 1. Purpose

Create a standardized CI/CD path that application teams can reuse rather than creating duplicate pipelines.

## 2. Workflow Stages

```mermaid
flowchart LR
    PR[Pull Request] --> Test[Unit Tests]
    Test --> TF[Terraform Validate]
    TF --> Secret[Gitleaks]
    Secret --> IaC[Checkov]
    IaC --> FS[Trivy Filesystem]
    FS --> Build[Container Build]
    Build --> Image[Trivy Image Scan]
    Image --> Review[Required Review]
    Review --> Release[Release Workflow]
```

## 3. Pull Request Controls

Pull requests must run:
- Application tests.
- Terraform formatting and validation.
- Gitleaks.
- Checkov.
- Trivy filesystem scanning.
- Container build.
- Trivy container scanning.

## 4. Release Controls

The release workflow must:
- Require explicit environment selection.
- Build from the reviewed source revision.
- Avoid printing credentials.
- Use environment protection for production when configured.
- Keep deployment credentials outside repository files.

## 5. GitHub Actions Security

Use:
- `permissions: contents: read` as the default baseline where possible.
- Job-specific permissions only when required.
- OIDC/federated credentials for cloud authentication when available instead of long-lived access keys.
- Reviewed and versioned third-party actions.

## 6. Failure Policy

A mandatory quality/security gate failing must fail the workflow. Exceptions require the governance process and must not silently bypass the check.

## 7. Reusability

Shared workflows should be designed as reusable workflows or centrally maintained workflow components where the GitHub organization permits it. Application repositories should supply parameters rather than copy platform implementation.

## 8. Acceptance Criteria

The workflow specification is satisfied when a pull request receives consistent automated validation and security feedback and the release path is separated from pull-request validation.
