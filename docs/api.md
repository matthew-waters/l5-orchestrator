# API Contracts (MVP)

All endpoints require `X-API-Key`.

## Clients
`POST /v1/clients`
```json
{ "name": "acme" }
```
Response:
```json
{ "id": "client_id", "api_key": "raw_key_once", "status": "active" }
```

`PUT /v1/clients/{client_id}/aws`
```json
{
  "role_arn": "arn:aws:iam::123:role/client",
  "external_id": "ext",
  "region_default": "us-east-1",
  "session_name_template": "orch-{client_id}"
}
```

## Artifacts
`POST /v1/artifacts/upload` (multipart/form-data)
- file: app.zip
- version: 1.0.0
Response:
```json
{
  "artifact_id": "artifact_id",
  "s3_uri": "s3://orchestrator-artifacts/{client_id}/app.zip",
  "sha256": "hex",
  "version": "1.0.0"
}
```

## Job Templates
`POST /v1/job-templates`
```json
{
  "name": "daily-etl",
  "app_artifact_id": "artifact_id",
  "default_args": {"arg1": "value"},
  "data_uri": "s3://bucket/data",
  "fleet_template_id": "m5.4xlarge"
}
```

## Job Requests
`POST /v1/jobs`
One-time:
```json
{
  "job_template_id": "template_id",
  "type": "ONE_TIME",
  "intended_time": "2026-01-25T12:00:00Z",
  "risk_mode": "NEUTRAL"
}
```
Reschedulable:
```json
{
  "job_template_id": "template_id",
  "type": "RESCHEDULABLE",
  "earliest_start": "2026-01-26T00:00:00Z",
  "latest_finish": "2026-01-27T00:00:00Z",
  "risk_mode": "CONSERVATIVE",
  "weights": {"carbon": 0.5, "risk": 0.4, "slack": 0.1}
}
```

## Scheduling Preview
`POST /v1/schedules/preview`
```json
{
  "job_template_id": "template_id",
  "fleet_template_id": "m5.4xlarge",
  "earliest_start": "2026-01-26T00:00:00Z",
  "latest_finish": "2026-01-27T00:00:00Z",
  "risk_mode": "NEUTRAL"
}
```
Response:
```json
{
  "candidates": [
    {
      "proposed_start": "2026-01-26T01:00:00Z",
      "estimated_finish_p50": "2026-01-26T02:00:00Z",
      "estimated_finish_p90": "2026-01-26T02:30:00Z",
      "scores": {"carbon": 0.2, "risk": 0.3, "slack": 0.8}
    }
  ],
  "chosen": {
    "proposed_start": "2026-01-26T01:00:00Z",
    "estimated_finish_p50": "2026-01-26T02:00:00Z",
    "estimated_finish_p90": "2026-01-26T02:30:00Z",
    "scores": {"carbon": 0.2, "risk": 0.3, "slack": 0.8}
  },
  "rationale": "selected by risk mode"
}
```

## Predictions
`GET /v1/predictions/runtime?job_template_id=...&fleet_template_id=...`
Response (available):
```json
{ "available": true, "p50_sec": 1800, "p90_sec": 2600, "confidence": 0.72, "sample_size": 6 }
```
Response (not available):
```json
{ "available": false, "notes": "insufficient history" }
```

## Runs
`GET /v1/runs/{run_id}` returns run status.
`POST /v1/runs/{run_id}/cancel` attempts best-effort cancel.
