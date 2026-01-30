"""Planner tick task that runs planning steps."""

from __future__ import annotations

import logging

from src.domain.planning.anchor_snapshots import capture_anchor_snapshots
from src.domain.planning.forecast_refresh import refresh_forecasts
from src.domain.planning.occurrence_generation import generate_occurrences
from src.domain.planning.planning import plan_occurrences
from src.domain.planning.rescheduling import reschedule_occurrences
from src.domain.scheduler.task import ScheduledTask

logger = logging.getLogger(__name__)


class PlannerTickTask(ScheduledTask):
    name = "planner_tick"

    def __init__(self, interval_seconds: int) -> None:
        self.interval_seconds = interval_seconds

    def run(self) -> None:
        logger.info("Planner tick starting")
        refresh_forecasts()
        generate_occurrences()
        capture_anchor_snapshots()
        plan_occurrences()
        reschedule_occurrences()
        logger.info("Planner tick completed")
