"""Fleet service."""

from __future__ import annotations

from typing import Iterable

from fastapi import Depends
from sqlalchemy.orm import Session

from src.adapters.db.models import Fleet
from src.adapters.db.repositories.fleet_repo import FleetRepository
from src.adapters.db.session import get_db


class FleetService:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.repo = FleetRepository(session)

    def list(self) -> Iterable[Fleet]:
        return self.repo.list()
