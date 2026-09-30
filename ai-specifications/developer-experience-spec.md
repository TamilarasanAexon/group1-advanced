# Developer Experience Specification

## 1. Purpose

Create a paved path that reduces onboarding time and cognitive load while preserving engineering and security standards.

## 2. Developer Journey

### Step 1 — Create
Developer starts from the standard repository template.

### Step 2 — Configure
Developer supplies application metadata and approved platform parameters.

### Step 3 — Validate locally
Developer runs:

```bash
pytest -q
docker build -t <application>:local app
terraform -chdir=infrastructure fmt -check -recursive
terraform -chdir=infrastructure init -backend=false
terraform -chdir=infrastructure validate
```

### Step 4 — Pull request
Developer opens a PR and receives automated test, IaC and security feedback.

### Step 5 — Review
Code owners and application reviewers review business and engineering changes.

### Step 6 — Release
The release workflow packages the reviewed revision and uses environment-specific controls.

## 3. Developer Experience Principles

- Secure defaults.
- Few mandatory decisions.
- Clear commands.
- Fast local feedback.
- Consistent repository structure.
- Self-service documentation.
- Actionable CI errors.
- No requirement to understand every platform implementation detail.

## 4. Documentation Requirements

Every application must document:
- Purpose.
- Local setup.
- Test commands.
- Container commands.
- Infrastructure validation.
- Deployment/release process.
- Security expectations.
- Ownership.
- Troubleshooting.

## 5. Self-Service Model

The platform should provide reusable capabilities while allowing application teams to independently:
- Create repositories.
- Run validation.
- Understand failures.
- Configure approved parameters.
- Trigger approved release processes.

## 6. Success Measures

The platform should measure, where organizational telemetry becomes available:
- Time to first successful local build.
- Time to first successful PR.
- Onboarding effort.
- Pipeline failure categories.
- Reuse of shared modules/workflows.
- Security findings detected before merge.

## 7. Acceptance Criteria

A new developer should be able to follow the repository README from clone through local validation and understand how the application enters the standard CI/CD path without needing undocumented platform-team intervention.
