class PredictionService:
    def get_runtime_prediction(self, job_template_id, fleet_template_id):
        raise NotImplementedError

    def update_runtime_stats(self, run):
        raise NotImplementedError
