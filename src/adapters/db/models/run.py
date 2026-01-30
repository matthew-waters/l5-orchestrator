"""Run model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.base import Base
from src.adapters.db.models.enums import RunStatus


class Run(Base):
    __tablename__ = "runs"

    run_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    occurrence_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("occurrences.occurrence_id"), nullable=False, index=True
    )
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), nullable=False)
    emr_cluster_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    error_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    artifact_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("app_artifacts.artifact_id"), nullable=False, index=True
    )
    fleet_template_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("fleets.fleet_template_id"), nullable=False, index=True
    )
    runtime_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    data_features_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    occurrence: Mapped["Occurrence"] = relationship(
        "Occurrence", back_populates="runs"
    )
    artifact: Mapped["AppArtifact"] = relationship(
        "AppArtifact", back_populates="runs"
    )
    fleet: Mapped["Fleet"] = relationship("Fleet", back_populates="runs")
