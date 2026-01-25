class SchedulerService:
    def select_candidates(self, job_request, forecasts, runtime_distribution):
        raise NotImplementedError

    def choose_plan(self, candidates, risk_mode, weights):
        raise NotImplementedError
