"""Workload service."""

from __future__ import annotations

from typing import Iterable

from fastapi import Depends
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.adapters.db.models import AppArtifact, Fleet, Workload
from src.adapters.db.repositories.occurrence_repo import OccurrenceRepository
from src.adapters.db.repositories.workload_repo import WorkloadRepository
from src.adapters.db.session import get_db
from src.domain.planning.occurrence_generation import generate_occurrences
from src.domain.types.schedule_rules import ScheduleRules
from src.domain.types.user_preferences import UserPreferences


class WorkloadService:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.workloads = WorkloadRepository(session)
        self.occurrences = OccurrenceRepository(session)

    def get(self, tenant_id: int, workload_id: int) -> Workload | None:
        workload = self.workloads.get_by_id(workload_id)
        if workload is None or workload.tenant_id != tenant_id:
            return None
        return workload

    def list(self, tenant_id: int) -> Iterable[Workload]:
        return self.workloads.list_by_tenant(tenant_id)

    def create(
        self,
        tenant_id: int,
        *,
        name: str,
        description: str | None,
        tags_json: list[str] | None,
        artifact_id: int,
        fleet_template_id: int,
        schedule_rules_json: ScheduleRules,
        user_preferences_json: UserPreferences,
        manual_runtime_seconds: int | None,
    ) -> Workload:
        schedule_rules = self._validate_schedule_rules(schedule_rules_json)
        user_preferences = self._validate_user_preferences(user_preferences_json)
        self._validate_artifact(tenant_id, artifact_id)
        self._validate_fleet(fleet_template_id)

        workload = Workload(
            tenant_id=tenant_id,
            name=name,
            description=description,
            tags_json=tags_json,
            artifact_id=artifact_id,
            fleet_template_id=fleet_template_id,
            schedule_rules_json=schedule_rules.model_dump(),
            user_preferences_json=user_preferences.model_dump(),
            manual_runtime_seconds=manual_runtime_seconds,
            is_active=True,
        )
        workload = self.workloads.create(workload)

        occurrences = generate_occurrences(workload)
        self.occurrences.create_many(occurrences)
        return workload

    def _validate_schedule_rules(self, rules: ScheduleRules) -> ScheduleRules:
        try:
            return ScheduleRules.model_validate(rules)
        except ValidationError as exc:
            raise ValueError("schedule_rules_json is invalid") from exc

    def _validate_user_preferences(
        self, prefs: UserPreferences
    ) -> UserPreferences:
        try:
            return UserPreferences.model_validate(prefs)
        except ValidationError as exc:
            raise ValueError("user_preferences_json is invalid") from exc

    def _validate_artifact(self, tenant_id: int, artifact_id: int) -> None:
        artifact = self.session.get(AppArtifact, artifact_id)
        if artifact is None or artifact.tenant_id != tenant_id:
            raise ValueError("artifact_id is invalid for tenant")

    def _validate_fleet(self, fleet_template_id: int) -> None:
        fleet = self.session.get(Fleet, fleet_template_id)
        if fleet is None:
            raise ValueError("fleet_template_id is invalid")
