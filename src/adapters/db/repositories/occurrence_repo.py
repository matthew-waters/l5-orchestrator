"""Occurrence repository."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from src.adapters.db.models import Occurrence


class OccurrenceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_by_workload(self, workload_id: int) -> Iterable[Occurrence]:
        return (
            self.session.query(Occurrence)
            .filter(Occurrence.workload_id == workload_id)
            .order_by(Occurrence.occurrence_id)
            .all()
        )

    def create_many(self, occurrences: list[Occurrence]) -> None:
        if not occurrences:
            return
        self.session.add_all(occurrences)
        self.session.commit()
