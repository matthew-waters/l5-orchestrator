import time


def run_scheduler_loop(interval_seconds: int) -> None:
    while True:
        # TODO: identify jobs entering horizon and produce schedule plans
        time.sleep(interval_seconds)
