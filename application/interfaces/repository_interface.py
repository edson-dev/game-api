from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    async def query_header(self, request):
        query = request.headers.get("query").split()
        querable = {}
        for i in query:
            value = request.headers.get(i)
            if value:
                querable[i] = value
        return querable

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