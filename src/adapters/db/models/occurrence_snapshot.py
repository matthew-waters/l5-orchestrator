"""Occurrence snapshot model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.base import Base
from src.adapters.db.models.enums import SnapshotType


class OccurrenceSnapshot(Base):
    __tablename__ = "occurrence_snapshots"

    snapshot_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    occurrence_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("occurrences.occurrence_id"), nullable=False, index=True
    )
    snapshot_type: Mapped[SnapshotType] = mapped_column(
        Enum(SnapshotType), nullable=False
    )
    plan_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("plans.plan_id"), nullable=True, index=True
    )
    s3_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    occurrence: Mapped["Occurrence"] = relationship(
        "Occurrence", back_populates="snapshots"
    )
    plan: Mapped["Plan | None"] = relationship(
        "Plan", back_populates="snapshots"
    )
