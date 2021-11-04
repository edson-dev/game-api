from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    async def query_header(self, request):
        query = await self.params_list(request)
        queryable = {}
        for i in query:
            value = request.headers.get(i)
            if value:
                queryable[i] = value
        return queryable

    async def params_list(self, request):
        return request.headers.get("query").split() \
            if request.headers.get("query") is not None else []

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