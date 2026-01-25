from pydantic import BaseModel


class RuntimePredictionResponse(BaseModel):
    available: bool = True
    p50_sec: int | None = None
    p90_sec: int | None = None
    confidence: float | None = None
    sample_size: int | None = None
    notes: str | None = None
