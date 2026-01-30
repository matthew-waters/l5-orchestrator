"""Planning task stub."""

from __future__ import annotations

import logging

from src.domain.scheduler.task import ScheduledTask

logger = logging.getLogger(__name__)


class PlanningTask(ScheduledTask):
    name = "planning"

    def __init__(self, interval_seconds: int) -> None:
        self.interval_seconds = interval_seconds

    def run(self) -> None:
        logger.info("Planning task stub")
