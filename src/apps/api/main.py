"""FastAPI application entrypoint."""

from fastapi import FastAPI

app = FastAPI(title="L5 Orchestrator API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
