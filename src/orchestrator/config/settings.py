from pydantic import BaseModel


class Settings(BaseModel):
    env: str = "local"
    log_level: str = "INFO"
    db_url: str = "sqlite:///./orchestrator.db"
    api_key_header: str = "X-API-Key"

    artifact_bucket: str = "orchestrator-artifacts"
    aws_region_default: str = "us-east-1"
    assume_role_duration_sec: int = 3600

    forecast_refresh_minutes: int = 30
    scheduler_interval_minutes: int = 30
    scheduler_lock_window_minutes: int = 120

    class Config:
        env_prefix = "ORCH_"
