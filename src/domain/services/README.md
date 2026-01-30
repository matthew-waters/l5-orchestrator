# Domain Services

This directory contains service-layer modules that orchestrate domain logic
and persistence operations. Services coordinate repositories and validation
but do not contain infrastructure or transport-specific code.

## Typical responsibilities

- Input validation and guardrails
- Coordinating multiple repositories
- Applying domain rules before persistence
- Returning domain entities for API layers

## Current services

- `tenant_service.py`: tenant lookup and creation logic
- `workload_service.py`: workload creation, validation, and occurrence wiring
