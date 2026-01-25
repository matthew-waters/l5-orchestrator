from fastapi import FastAPI

from orchestrator.api.routers import artifacts, clients, jobs, predictions, runs, schedules, templates
from orchestrator.config.settings import Settings


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(title="Spark Job Orchestrator", version="0.1.0")
    app.state.settings = settings

    app.include_router(clients.router, prefix="/v1")
    app.include_router(artifacts.router, prefix="/v1")
    app.include_router(templates.router, prefix="/v1")
    app.include_router(jobs.router, prefix="/v1")
    app.include_router(schedules.router, prefix="/v1")
    app.include_router(predictions.router, prefix="/v1")
    app.include_router(runs.router, prefix="/v1")

    return app


app = create_app()
