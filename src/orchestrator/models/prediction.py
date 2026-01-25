from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from orchestrator.models.base import Base, TimestampMixin


class RuntimePrediction(Base, TimestampMixin):
    __tablename__ = "runtime_predictions"

    job_template_id: Mapped[str] = mapped_column(String, primary_key=True)
    fleet_template_id: Mapped[str] = mapped_column(String, primary_key=True)
    p50_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    p90_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    sample_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
