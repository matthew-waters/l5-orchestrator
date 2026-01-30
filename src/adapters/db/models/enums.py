"""Enum types for ORM models."""

from enum import Enum as PyEnum


class OccurrenceState(str, PyEnum):
    UNPLANNED = "UNPLANNED"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PlanStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    CANCELED = "CANCELED"


class RunStatus(str, PyEnum):
    QUEUED = "QUEUED"
    PROVISIONING = "PROVISIONING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class SnapshotType(str, PyEnum):
    AT_ANCHOR = "AT_ANCHOR"
    AT_PLAN_CREATED = "AT_PLAN_CREATED"
