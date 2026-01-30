"""Tenant model."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    tenant_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    api_key_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    aws_links: Mapped[List["AwsLink"]] = relationship(
        "AwsLink", back_populates="tenant"
    )
    app_artifacts: Mapped[List["AppArtifact"]] = relationship(
        "AppArtifact", back_populates="tenant"
    )
    workloads: Mapped[List["Workload"]] = relationship(
        "Workload", back_populates="tenant"
    )
