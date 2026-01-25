from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from orchestrator.models.base import Base, TimestampMixin


class JobRequest(Base, TimestampMixin):
    __tablename__ = "job_requests"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    client_id: Mapped[str] = mapped_column(String, nullable=False)
    job_template_id: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    intended_time: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    earliest_start: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    latest_finish: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    risk_mode: Mapped[str] = mapped_column(String, default="NEUTRAL")
    weights: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    state: Mapped[str] = mapped_column(String, default="PLANNED")
