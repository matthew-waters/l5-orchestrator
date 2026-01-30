"""Fleet model."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, DateTime, JSON, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.base import Base


class Fleet(Base):
    __tablename__ = "fleets"

    fleet_template_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    config_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    workloads: Mapped[List["Workload"]] = relationship(
        "Workload", back_populates="fleet"
    )
    runs: Mapped[List["Run"]] = relationship("Run", back_populates="fleet")
