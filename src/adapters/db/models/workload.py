"""Workload model."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.base import Base


class Workload(Base):
    __tablename__ = "workloads"

    workload_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tenants.tenant_id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    artifact_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("app_artifacts.artifact_id"), nullable=False, index=True
    )
    fleet_template_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("fleets.fleet_template_id"), nullable=False, index=True
    )
    schedule_rules_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    user_preferences_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    manual_runtime_seconds: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("1")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="workloads")
    artifact: Mapped["AppArtifact"] = relationship(
        "AppArtifact", back_populates="workloads"
    )
    fleet: Mapped["Fleet"] = relationship("Fleet", back_populates="workloads")
    occurrences: Mapped[List["Occurrence"]] = relationship(
        "Occurrence", back_populates="workload"
    )
