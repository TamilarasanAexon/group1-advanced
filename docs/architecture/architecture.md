# Group1 Advanced Architecture

## Overview

The `group1-advanced` capstone implements an automated DevSecOps delivery path for a Python API. Application code, tests, infrastructure definitions, container configuration, and GitHub Actions workflows are maintained in one repository.

The solution follows this lifecycle:

**Code → Test → Secure → Build → Release → Deploy → Validate**

## Solution Architecture

```mermaid
flowchart TB
    DEV["Developer<br/>Python • Terraform • Docker • Git"]

    REPO["GitHub Repository<br/>group1-advanced<br/><br/>Application Code<br/>Terraform IaC<br/>Dockerfile<br/>Automated Tests<br/>GitHub Actions Workflows"]

    subgraph CI["CI and DevSecOps Pipeline • ci.yml"]
        direction TB

        PY["Python and API Tests<br/><br/>Syntax Validation<br/>Import Validation<br/>Pytest<br/>API Startup<br/>Health Check"]

        TF["Terraform Validation<br/><br/>terraform fmt<br/>terraform init<br/>terraform validate"]

        subgraph SECURITY["Security Controls"]
            direction LR
            GL["Gitleaks<br/>Secret Detection"]
            CK["Checkov<br/>IaC Security"]
            TVFS["Trivy<br/>Filesystem Scan"]

            GL --> CK --> TVFS
        end

        DOCKER["Container Validation<br/><br/>Docker Build<br/>Container Startup<br/>API Health Test<br/>Trivy Image Scan"]

        PY --> SECURITY
        TF --> SECURITY
        SECURITY --> DOCKER
    end

    subgraph IAC["Infrastructure Definition and Validation"]
        direction TB
        VPC["AWS VPC"]
        SUBNET["Private Subnet"]
        SG["Security Groups"]
        FLOW["VPC Flow Logs"]
        CW["CloudWatch Logs<br/>365-Day Retention"]
        KMS["KMS Encryption<br/>Key Rotation"]

        VPC --> SUBNET
        VPC --> SG
        VPC --> FLOW
        FLOW --> CW
        KMS --> CW
    end

    RELEASE["Release Pipeline • release.yml<br/><br/>Build Release Image<br/>Trivy Security Scan<br/>Apply Version and SHA Tags<br/>Publish Container"]

    GHCR["GitHub Container Registry<br/>GHCR<br/><br/>Version Tag<br/>Commit SHA Tag<br/>Latest Tag"]

    DEPLOY["Development Deployment • deploy.yml<br/><br/>GitHub Environment: dev<br/>Authenticate to GHCR<br/>Pull Release Image<br/>Start Container<br/>Expose Port 8080"]

    VALIDATE["Health and API Validation<br/><br/>GET /health → status: ok<br/>GET / → API response<br/>GET /doc → Documentation<br/>Pytest → Tests passing"]

    SUCCESS["Deployment Successful"]

    DEV -->|"git push"| REPO
    REPO --> PY
    REPO --> TF
    REPO -.->|"Terraform definitions"| IAC

    DOCKER -->|"All quality gates pass"| RELEASE
    RELEASE -->|"Publish image"| GHCR
    GHCR -->|"Pull selected image tag"| DEPLOY
    DEPLOY --> VALIDATE
    VALIDATE --> SUCCESS

    classDef developer fill:#163A5F,color:#FFFFFF,stroke:#0B2239,stroke-width:2px;
    classDef repository fill:#1F4E78,color:#FFFFFF,stroke:#163A5F,stroke-width:2px;
    classDef pipeline fill:#D9EAF7,color:#102A43,stroke:#2F75B5,stroke-width:2px;
    classDef terraform fill:#E4DAF5,color:#3B245F,stroke:#7654A8,stroke-width:2px;
    classDef security fill:#FCE4D6,color:#7F2704,stroke:#E46C0A,stroke-width:2px;
    classDef container fill:#DDEBF7,color:#12344D,stroke:#00A4EF,stroke-width:2px;
    classDef registry fill:#E7E6E6,color:#202020,stroke:#595959,stroke-width:2px;
    classDef deployment fill:#E2F0D9,color:#1F4E20,stroke:#548235,stroke-width:2px;
    classDef success fill:#70AD47,color:#FFFFFF,stroke:#385723,stroke-width:3px;

    class DEV developer;
    class REPO repository;
    class PY pipeline;
    class TF,VPC,SUBNET,SG,FLOW,CW,KMS terraform;
    class GL,CK,TVFS security;
    class DOCKER container;
    class RELEASE pipeline;
    class GHCR registry;
    class DEPLOY,VALIDATE deployment;
    class SUCCESS success;
```

## Presentation View

```mermaid
flowchart LR
    DEV["Developer"] --> REPO["GitHub Repository"]
    REPO --> CI["CI Pipeline<br/>Python • Pytest • Terraform"]
    CI --> SEC["Security Gates<br/>Gitleaks • Checkov • Trivy"]
    SEC --> BUILD["Docker Build<br/>Container Test"]
    BUILD --> RELEASE["Release Pipeline"]
    RELEASE --> GHCR["GitHub Container Registry"]
    GHCR --> DEPLOY["Dev Deployment"]
    DEPLOY --> HEALTH["Health and API Validation"]
    HEALTH --> SUCCESS["Deployment Successful"]

    REPO -.-> IAC["Terraform Infrastructure Definition<br/>VPC • Subnet • Security Groups<br/>Flow Logs • CloudWatch • KMS"]

    classDef primary fill:#1F4E78,color:#FFFFFF,stroke:#163A5F,stroke-width:2px;
    classDef security fill:#F4B183,color:#5B2700,stroke:#C65911,stroke-width:2px;
    classDef deploy fill:#A9D18E,color:#1F4E20,stroke:#548235,stroke-width:2px;
    classDef infrastructure fill:#D9EAD3,color:#274E13,stroke:#6AA84F,stroke-width:2px;

    class DEV,REPO,CI,BUILD,RELEASE,GHCR primary;
    class SEC security;
    class DEPLOY,HEALTH,SUCCESS deploy;
    class IAC infrastructure;
```

## Component Responsibilities

### GitHub Repository

- Stores the Python API, tests, Dockerfile, Terraform modules, and documentation.
- Stores `ci.yml`, `release.yml`, and `deploy.yml` under `.github/workflows/`.

### CI and DevSecOps Pipeline

- Validates Python syntax and imports.
- Starts the API and runs automated tests.
- Formats, initializes, and validates Terraform.
- Runs Gitleaks, Checkov, and Trivy security checks.
- Builds the Docker image and validates the running container.

### Infrastructure Definition

- Defines the VPC, private subnet, security controls, VPC Flow Logs, CloudWatch logging, and KMS encryption.
- Represents infrastructure definition and validation. It does not imply that the capstone provisioned live AWS infrastructure.

### Release Pipeline

- Builds the release container image.
- Scans the image with Trivy.
- Publishes version, commit SHA, and latest tags to GHCR.

### Development Deployment

- Uses the GitHub `dev` environment.
- Authenticates to GHCR and pulls the selected image tag.
- Runs the container on port 8080.

### Health and API Validation

- Checks `GET /health` for `status: ok`.
- Checks the root API endpoint at `GET /`.
- Checks the documentation endpoint at `GET /doc`.
- Marks deployment successful only after validation passes.
