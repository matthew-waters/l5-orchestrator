class SpotForecastProvider:
    def fetch(self, region: str, fleet_template_id: str, start, end):
        raise NotImplementedError
