# Platform Architecture

```mermaid
flowchart LR
    Dev[Application Team] --> Repo[Standard Repository Template]
    Repo --> CI[GitHub Actions]
    CI --> Test[Tests]
    CI --> Sec[Security Gates]
    CI --> TF[Terraform Validation]
    Repo --> Modules[Reusable Terraform Modules]
    CI --> Release[Release Workflow]
    Release --> Runtime[AWS / Local Runtime]
    Platform[Platform Team] --> Repo
    Platform --> CI
    Platform --> Modules
    Platform --> Standards[Engineering Standards]
```

## Platform layers
- Developer experience: templates, README, local commands.
- Delivery: reusable GitHub Actions.
- Infrastructure: reusable Terraform modules.
- Security: Gitleaks, Checkov, Trivy.
- Governance: ADRs, ownership, exception process.
