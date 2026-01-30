"""Occurrence model."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.base import Base
from src.adapters.db.models.enums import OccurrenceState


class Occurrence(Base):
    __tablename__ = "occurrences"

    occurrence_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    workload_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("workloads.workload_id"), nullable=False, index=True
    )
    anchor_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deadline_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    state: Mapped[OccurrenceState] = mapped_column(
        Enum(OccurrenceState), nullable=False
    )
    locked: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("0")
    )
    current_plan_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("plans.plan_id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    workload: Mapped["Workload"] = relationship(
        "Workload", back_populates="occurrences"
    )
    current_plan: Mapped["Plan | None"] = relationship(
        "Plan", foreign_keys=[current_plan_id], post_update=True
    )
    plans: Mapped[List["Plan"]] = relationship(
        "Plan", back_populates="occurrence", foreign_keys="Plan.occurrence_id"
    )
    snapshots: Mapped[List["OccurrenceSnapshot"]] = relationship(
        "OccurrenceSnapshot", back_populates="occurrence"
    )
    runs: Mapped[List["Run"]] = relationship("Run", back_populates="occurrence")
