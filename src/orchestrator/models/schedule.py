from sqlalchemy import JSON, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from orchestrator.models.base import Base, TimestampMixin


class SchedulePlan(Base, TimestampMixin):
    __tablename__ = "schedule_plans"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    job_request_id: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, default="PLANNED")
    chosen_start_time: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    candidate_set: Mapped[list | None] = mapped_column(JSON, nullable=True)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    locked_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
