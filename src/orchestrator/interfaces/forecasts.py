from abc import ABC, abstractmethod


class ForecastProvider(ABC):
    @abstractmethod
    def get_forecast(self, region: str, start, end):
        raise NotImplementedError
