from abc import ABC, abstractmethod


class ClusterBackend(ABC):
    @abstractmethod
    def launch_cluster(self, spec):
        raise NotImplementedError

    @abstractmethod
    def submit_job(self, cluster_id, step_spec):
        raise NotImplementedError

    @abstractmethod
    def get_status(self, cluster_id, step_id):
        raise NotImplementedError

    @abstractmethod
    def terminate_cluster(self, cluster_id):
        raise NotImplementedError
