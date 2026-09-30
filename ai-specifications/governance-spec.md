# Governance Specification

## 1. Purpose

Establish lightweight controls that protect security, consistency and maintainability without turning the platform team into a manual approval bottleneck.

## 2. Ownership

Every shared platform component must have:
- An owning team.
- Maintainer documentation.
- A defined change process.
- A versioning strategy.

## 3. Required Controls

- Pull requests for changes to platform-owned assets.
- Required CI and security checks.
- CODEOWNERS for critical shared paths where supported.
- ADRs for material architectural decisions.
- Secret-management controls.
- Documentation for breaking changes.
- Periodic review of security exceptions.

## 4. Exception Process

An exception must document:

```text
Request
Owner
Reason
Affected component
Security impact
Scope
Start date
Expiry/review date
Mitigation
Approver
```

Exceptions must be temporary and reviewable rather than becoming permanent undocumented bypasses.

## 5. Change Management

### Standard change
Backward-compatible change with tests and documentation.

### Breaking change
Requires:
- Explicit version/change notice.
- Migration instructions.
- Impacted consumers identified.
- Updated documentation.

## 6. AI-Generated Artifact Governance

AI-generated code and specifications are treated as engineering artifacts, not automatically trusted output. Before adoption they must be:
- Reviewed by an engineer.
- Tested.
- Security scanned.
- Checked against the relevant specification.
- Documented where design decisions are material.

## 7. Acceptance Criteria

Governance is effective when reviewers can identify ownership, required controls, exception handling and the decision history for significant platform changes.
