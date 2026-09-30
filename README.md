# Group1 Advanced

A DevSecOps-oriented Python API project with automated testing, Terraform validation, containerization, and security scanning.

## Overview

`group1-advanced` demonstrates a practical CI/CD and DevSecOps workflow around a lightweight Python HTTP API. The project is designed to validate application code, infrastructure as code, container builds, and common security controls through GitHub Actions.

## Key Features

- Python HTTP API
- Health-check endpoint for automated readiness validation
- Automated Python syntax validation and tests
- Docker container build
- Terraform infrastructure validation
- Gitleaks secret scanning
- Checkov infrastructure-as-code security scanning
- Trivy filesystem and container vulnerability scanning
- GitHub Actions CI pipeline

## Technology Stack

| Area | Technology |
|---|---|
| Application | Python 3.12 |
| API Server | Python `http.server` / `HTTPServer` |
| Testing | pytest |
| Containers | Docker |
| Infrastructure as Code | Terraform |
| CI/CD | GitHub Actions |
| Secret Detection | Gitleaks |
| IaC Security | Checkov |
| Vulnerability Scanning | Trivy |

## Repository Structure

```text
group1-advanced/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt        # if application dependencies are required
├── infrastructure/
│   ├── main.tf                 # root Terraform configuration, if used
│   ├── variables.tf            # root variables, if used
│   ├── outputs.tf              # root outputs, if used
│   └── modules/
│       ├── application-baseline/
│       ├── networking/
│       └── security/
├── tests/                      # pytest tests, if present
├── requirements.txt            # project dependencies, if used
└── README.md
```

> The exact Terraform files and test files may vary. Keep this section aligned with the repository as the project evolves.

## API Endpoints

The current application is expected to run on port `8080`.

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Application/API information |
| `/health` | GET | API health check |
| `/doc` | GET | Basic API endpoint information, when implemented in `main.py` |

### Health Check

Expected successful health response:

```json
{"status": "ok"}
```

## Prerequisites

For full local validation, install the tools relevant to the checks you want to run:

- Git
- Python 3.12 or compatible project version
- pip
- Docker
- Terraform

Security scanners are executed by the GitHub Actions workflow when configured there, so local installation of Gitleaks, Checkov, or Trivy is optional unless you want to run those scans locally.

## Run the API Locally

### 1. Clone and enter the repository

```bash
git clone <repository-url>
cd group1-advanced
```

On the existing Windows workspace used during development:

```cmd
cd C:\group1-advanced\group1-advanced
```

### 2. Create a virtual environment

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If a root `requirements.txt` exists:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If dependencies are maintained under `app/requirements.txt` instead:

```bash
pip install -r app/requirements.txt
```

For test execution, ensure pytest is installed:

```bash
pip install pytest
```

### 4. Validate Python syntax

```bash
python -m py_compile app/main.py
```

No output indicates that the file compiled without a reported syntax error.

### 5. Start the API

```bash
python app/main.py
```

The development server should listen on port `8080` according to the current project configuration.

### 6. Verify the health endpoint

Open another terminal.

Windows:

```cmd
curl --noproxy "*" -i http://127.0.0.1:8080/health
```

Linux/macOS:

```bash
curl -i http://127.0.0.1:8080/health
```

Expected body:

```json
{"status": "ok"}
```

You can also open the application locally in a web browser at `http://127.0.0.1:8080/`.

## Run Tests

From the repository root:

```bash
python -m pytest -v
```

Before committing application changes, it is useful to run both checks:

```bash
python -m py_compile app/main.py
python -m pytest -v
```

## Docker

The CI design builds the application using `app/Dockerfile`.

### Build locally

From the repository root:

```bash
docker build -t group1-advanced:local -f app/Dockerfile app
```

### Run locally

```bash
docker run --rm -p 8080:8080 group1-advanced:local
```

Then verify:

```bash
curl -i http://127.0.0.1:8080/health
```

## Terraform

Terraform configuration is stored under `infrastructure/`.

### Format

```bash
terraform -chdir=infrastructure fmt -recursive
```

### Initialize without configuring a backend

```bash
terraform -chdir=infrastructure init -backend=false
```

### Validate

```bash
terraform -chdir=infrastructure validate
```

A successful validation reports that the Terraform configuration is valid.

### Module Output Naming

Terraform output names must be unique within a module. For the `application-baseline` module, define `application_name` only once. A clean pattern is:

`modules/application-baseline/main.tf`:

```hcl
locals {
  application_name = "${var.project_name}-${var.environment}"
}
```

`modules/application-baseline/outputs.tf`:

```hcl
output "application_name" {
  description = "Standardized application name."
  value       = local.application_name
}
```

Do not repeat the same `output "application_name"` block in `main.tf` and `outputs.tf`.

## CI/CD Pipeline

The GitHub Actions workflow is maintained in:

```text
.github/workflows/ci.yml
```

The intended pipeline covers the following stages:

1. Checkout source code
2. Set up Python
3. Install dependencies
4. Validate `app/main.py` syntax
5. Start the API
6. Verify `/health`
7. Run automated tests
8. Format and validate Terraform
9. Run security scans
10. Build the Docker image
11. Scan the container image

## Security Scanning

### Gitleaks

Gitleaks is used to detect credentials, tokens, API keys, and other secrets that may have been committed to the repository.

Recommended practice:

- Never commit real credentials.
- Use GitHub Secrets or another approved secret-management solution.
- If a real secret is exposed, rotate/revoke it rather than only deleting it from the latest commit.

### Checkov

Checkov scans Terraform and other infrastructure-as-code configuration for security and configuration issues.

For this repository, the primary scan target is:

```text
infrastructure/
```

### Trivy

Trivy is used for vulnerability scanning. The project CI can use it in two places:

- Filesystem/repository scanning
- Docker image scanning

The configured security gate can be set to fail on `HIGH` and `CRITICAL` findings.

## Suggested GitHub Actions Security Job

```yaml
security:
  name: Security Scans
  runs-on: ubuntu-latest

  permissions:
    contents: read
    security-events: write
    actions: read

  steps:
    - name: Checkout repository
      uses: actions/checkout@v6
      with:
        fetch-depth: 0

    - name: Gitleaks Secret Scan
      uses: gitleaks/gitleaks-action@v3
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Checkov IaC Scan
      uses: bridgecrewio/checkov-action@v12
      with:
        directory: infrastructure
        framework: terraform
        quiet: true
        compact: true

    - name: Trivy Filesystem Scan
      uses: aquasecurity/trivy-action@v0.36.0
      with:
        scan-type: fs
        scan-ref: .
        format: table
        severity: CRITICAL,HIGH
        ignore-unfixed: true
        exit-code: "1"
```

## Troubleshooting

### API does not start

Validate syntax first:

```bash
python -m py_compile app/main.py
```

Then start the API directly so the complete traceback is visible:

```bash
python app/main.py
```

Common items to check include invalid Python syntax, an already-used port, missing dependencies, or a mismatch between the application port and the CI health check.

### CI displays `Waiting for API...`

The health-check loop normally means the CI runner cannot successfully reach:

```text
http://127.0.0.1:8080/health
```

Check the application log emitted by the workflow. A Python exception during startup must be fixed before the health check can succeed.

### Terraform duplicate output definition

An error similar to:

```text
Error: Duplicate output definition
```

means the same output name exists more than once within a Terraform module. Keep only one definition for each output name.

After correcting Terraform files:

```bash
terraform -chdir=infrastructure fmt -recursive
terraform -chdir=infrastructure init -backend=false
terraform -chdir=infrastructure validate
```

### Port 8080 already in use on Windows

Check the process using the port:

```cmd
netstat -ano | findstr :8080
```

Use the PID shown by the command to identify the process before deciding whether it should be stopped.

## Development Workflow

A practical local workflow is:

```bash
python -m py_compile app/main.py
python -m pytest -v
terraform -chdir=infrastructure fmt -check -recursive
terraform -chdir=infrastructure init -backend=false
terraform -chdir=infrastructure validate
docker build -t group1-advanced:local -f app/Dockerfile app
```

After successful local validation:

```bash
git status
git add .
git commit -m "Update application and DevSecOps pipeline"
git push
```

## Security Principles

This project follows a shift-left DevSecOps approach by integrating validation and security controls into the development workflow.

Key principles include:

- Validate code before deployment.
- Treat infrastructure as version-controlled code.
- Prevent secrets from being committed.
- Scan infrastructure configuration for security issues.
- Scan application dependencies and container images for known vulnerabilities.
- Use CI security checks as deployment quality gates.
- Keep dependencies, Actions, and scanner versions maintained.

## Project Status

Active development and CI/CD validation.

Current focus areas include:

- API stability and health checking
- Automated Python testing
- Terraform module validation
- Docker image validation
- DevSecOps security scanning with Gitleaks, Checkov, and Trivy

## Contributing

When contributing:

1. Create a working branch.
2. Make focused changes.
3. Validate Python and Terraform locally.
4. Run tests.
5. Do not commit secrets or generated sensitive files.
6. Push the branch and allow CI/security checks to complete.
7. Resolve failing quality or security gates before merge.

## License

No license has been specified in the information available for this project. Add an appropriate `LICENSE` file and update this section if the repository is intended for distribution.

## Disclaimer

This repository is a project/demo implementation. Review application, infrastructure, container, and security configurations against your organization's production requirements before using them in a production environment.
