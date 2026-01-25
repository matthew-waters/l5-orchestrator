import time


def run_execution_loop(interval_seconds: int) -> None:
    while True:
        # TODO: launch scheduled jobs and update run status
        time.sleep(interval_seconds)
