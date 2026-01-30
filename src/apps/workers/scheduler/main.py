"""Periodic scheduler worker entrypoint."""

from __future__ import annotations

import logging
import os
import signal
from threading import Event

from dotenv import load_dotenv

from src.domain.tasks.planning.planner_tick import PlannerTickTask
from src.domain.scheduler.engine import SchedulerEngine


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    tick_minutes = _get_int("SCHEDULER_TICK_MINUTES", 1)
    planner_interval_minutes = _get_int("PLANNER_TICK_INTERVAL_MINUTES", 30)
    tick_seconds = tick_minutes * 60
    planner_interval = planner_interval_minutes * 60

    tasks = [
        PlannerTickTask(interval_seconds=planner_interval),
    ]

    stop_event = Event()

    def _handle_signal(_: int, __: object) -> None:
        stop_event.set()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    SchedulerEngine(tasks=tasks, tick_seconds=tick_seconds).run_forever(stop_event)


if __name__ == "__main__":
    main()
