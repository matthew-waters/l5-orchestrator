class EmrClient:
    def create_cluster(self, config):
        raise NotImplementedError

    def add_step(self, cluster_id, step_config):
        raise NotImplementedError

    def get_step_status(self, cluster_id, step_id):
        raise NotImplementedError

    def terminate_cluster(self, cluster_id):
        raise NotImplementedError
