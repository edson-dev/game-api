from abc import ABC, abstractmethod


class RepositoryInterface(ABC):

    def __init__(self, app, repository, access_point="/repository"):
        self.init_app(app, repository, access_point)

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