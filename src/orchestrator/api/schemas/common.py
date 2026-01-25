from enum import Enum
from typing import Any

from pydantic import BaseModel


class JobType(str, Enum):
    one_time = "ONE_TIME"
    reschedulable = "RESCHEDULABLE"


class JobState(str, Enum):
    planned = "PLANNED"
    locked = "LOCKED"
    running = "RUNNING"
    completed = "COMPLETED"
    failed = "FAILED"
    cancelled = "CANCELLED"


class RiskMode(str, Enum):
    optimistic = "OPTIMISTIC"
    neutral = "NEUTRAL"
    conservative = "CONSERVATIVE"


class RunStatus(str, Enum):
    pending = "PENDING"
    provisioning = "PROVISIONING"
    submitted = "SUBMITTED"
    running = "RUNNING"
    succeeded = "SUCCEEDED"
    failed = "FAILED"
    cancelled = "CANCELLED"


class Metadata(BaseModel):
    data: dict[str, Any] = {}
