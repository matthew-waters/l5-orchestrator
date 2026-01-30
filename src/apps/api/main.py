"""FastAPI application entrypoint."""

from fastapi import FastAPI

from src.apps.api.routes.tenants import router as tenants_router
from src.apps.api.routes.workloads import router as workloads_router

app = FastAPI(title="L5 Orchestrator API")
app.include_router(tenants_router)
app.include_router(workloads_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
