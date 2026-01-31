"""Fleet repository."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from src.adapters.db.models import Fleet


class FleetRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, fleet_template_id: int) -> Fleet | None:
        return self.session.get(Fleet, fleet_template_id)

    def list(self) -> Iterable[Fleet]:
        return self.session.query(Fleet).order_by(Fleet.fleet_template_id).all()

    def create(self, fleet: Fleet) -> Fleet:
        self.session.add(fleet)
        self.session.commit()
        self.session.refresh(fleet)
        return fleet
