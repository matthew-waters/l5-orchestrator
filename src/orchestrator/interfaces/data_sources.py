from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def resolve_uri(self, uri: str):
        raise NotImplementedError

    @abstractmethod
    def validate_access(self, uri: str):
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self, uri: str):
        raise NotImplementedError
