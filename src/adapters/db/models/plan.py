"""Plan model."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.base import Base
from src.adapters.db.models.enums import PlanStatus


class Plan(Base):
    __tablename__ = "plans"

    plan_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    occurrence_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("occurrences.occurrence_id"), nullable=False, index=True
    )
    status: Mapped[PlanStatus] = mapped_column(Enum(PlanStatus), nullable=False)
    planned_start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    occurrence: Mapped["Occurrence"] = relationship(
        "Occurrence", back_populates="plans", foreign_keys=[occurrence_id]
    )
    snapshots: Mapped[List["OccurrenceSnapshot"]] = relationship(
        "OccurrenceSnapshot", back_populates="plan"
    )
