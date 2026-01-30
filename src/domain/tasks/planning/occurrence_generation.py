"""Occurrence generation task stub."""

from __future__ import annotations

import logging

from src.domain.scheduler.task import ScheduledTask

logger = logging.getLogger(__name__)


class OccurrenceGenerationTask(ScheduledTask):
    name = "occurrence_generation"

    def __init__(self, interval_seconds: int) -> None:
        self.interval_seconds = interval_seconds

    def run(self) -> None:
        logger.info("Occurrence generation task stub")
