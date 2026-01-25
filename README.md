# Spark Job Orchestrator (MVP Scaffold)

Always-on orchestrator service for scheduling and running PySpark jobs on EMR.
This repository contains the initial scaffold: API routes, data models, and
worker service stubs.

## Stack
- FastAPI + Uvicorn
- SQLite (MVP)
- SQLAlchemy + Pydantic
- Boto3 (AWS)

## Quickstart (local)
1) Create a virtualenv and install deps
2) `uvicorn orchestrator.main:app --reload`

## Configuration
Environment variables are documented in `.env.example`.

## Structure
Source lives under `src/orchestrator`. See `docs/architecture.md` and
`docs/api.md` for design details and API contracts.
