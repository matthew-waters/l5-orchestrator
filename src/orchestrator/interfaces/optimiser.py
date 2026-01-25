from abc import ABC, abstractmethod


class Optimiser(ABC):
    @abstractmethod
    def compute_candidates(self, window, forecasts, runtime_distribution, weights):
        raise NotImplementedError

    @abstractmethod
    def choose_candidate(self, candidates, risk_mode, weights):
        raise NotImplementedError
