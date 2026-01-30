"""Task interface for the scheduler."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ScheduledTask(ABC):
    name: str
    interval_seconds: int

    @abstractmethod
    def run(self) -> None:
        """Run the task once."""
