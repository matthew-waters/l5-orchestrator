import time


def run_forecast_refresher(interval_seconds: int) -> None:
    while True:
        # TODO: fetch and cache carbon + spot forecasts
        time.sleep(interval_seconds)
