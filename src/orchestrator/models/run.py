from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from orchestrator.models.base import Base, TimestampMixin


class Run(Base, TimestampMixin):
    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    job_request_id: Mapped[str] = mapped_column(String, nullable=False)
    schedule_plan_id: Mapped[str | None] = mapped_column(String, nullable=True)
    resolved_args: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    data_uri: Mapped[str | None] = mapped_column(Text, nullable=True)
    emr_cluster_id: Mapped[str | None] = mapped_column(String, nullable=True)
    emr_step_id: Mapped[str | None] = mapped_column(String, nullable=True)
    logs_uri: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="PENDING")
    started_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    runtime_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
