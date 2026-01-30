"""Workload repository."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from src.adapters.db.models import Workload


class WorkloadRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, workload_id: int) -> Workload | None:
        return self.session.get(Workload, workload_id)

    def list_by_tenant(self, tenant_id: int) -> Iterable[Workload]:
        return (
            self.session.query(Workload)
            .filter(Workload.tenant_id == tenant_id)
            .order_by(Workload.workload_id)
            .all()
        )

    def create(self, workload: Workload) -> Workload:
        self.session.add(workload)
        self.session.commit()
        self.session.refresh(workload)
        return workload
