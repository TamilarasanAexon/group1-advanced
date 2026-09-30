# ADR-002: Local-First Validation

## Context
The participant guide states that cloud infrastructure may not be provided and the submission should be reproducible without dedicated cloud resources.

## Decision
All core validation must work locally using Docker, Terraform validation and open-source/local alternatives where required.

## Consequences
The project remains demonstrable without an AWS account while preserving AWS as the preferred target architecture.
