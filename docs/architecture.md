# Architecture (MVP)

## Services
- API (FastAPI): handles client auth, artifacts, templates, job requests, previews.
- Scheduler loop: selects plans for reschedulable jobs within 48h horizon.
- Execution loop: launches EMR, submits steps, tracks status, collects logs.
- Forecast refresher: caches carbon and spot forecasts.
- Prediction engine: updates runtime estimates after runs complete.

## Scheduling Semantics
- Evaluate when `earliest_start <= now + 48h`.
- Re-run scheduling on forecast update or every 30–60 minutes.
- Lock plan when chosen start time is within a short commit window
  (default 2 hours) or forecast stability thresholds are met.
- State transitions: `PLANNED → LOCKED → RUNNING → COMPLETED/FAILED`.

## Data Flow Summary
- CLI uploads `app.zip` to orchestrator, which stores it in an artifacts bucket.
- User submits a job request referencing a job template and data URI.
- For reschedulable jobs, the scheduler computes Pareto candidates and locks a plan.
- Execution loop assumes client role, creates EMR cluster, submits spark step, monitors, terminates.

## Extensibility Interfaces
- `ForecastProvider`: carbon + spot implementations.
- `ClusterBackend`: EMR on EC2 now, EMR Serverless later.
- `DataSource`: S3 now, extensible to other sources.
- `Optimiser`: Pareto frontier + risk-mode scoring policy.

## Security
- API key authentication (per client), stored as hash.
- STS AssumeRole with external ID and short sessions.
- Per-client S3 prefixes for artifact isolation.
