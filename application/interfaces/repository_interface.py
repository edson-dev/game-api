from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    @abstractmethod
    def init_app(self):
        """Initialize the factory method"""
        raise NotImplemented

    def create(self):
        raise NotImplemented

    def read(self):
        raise NotImplemented

    def update(self):
        raise NotImplemented

    def delete(self):
        raise NotImplemented