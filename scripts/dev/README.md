# Developer Scripts

## run_api.py

Launches the FastAPI application using Uvicorn.

Run:

```bash
python -m scripts.dev.run_api
```

Env:

- `API_HOST` (default `0.0.0.0`)
- `API_PORT` (default `8000`)
- `API_RELOAD` (default `true`)

## run_scheduler.py

Runs the periodic scheduler worker (planner tick).

Run:

```bash
python -m scripts.dev.run_scheduler
```

Env:

- `SCHEDULER_TICK_SECONDS` (default `30`)
- `PLANNER_TICK_INTERVAL_SECONDS` (default `1800`)

## run_executor.py

Runs the always-on executor worker.

Run:

```bash
python -m scripts.dev.run_executor
```

Env:

- `EXECUTOR_POLL_SECONDS` (default `15`)
