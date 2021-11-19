from abc import ABC, abstractmethod

from bson import ObjectId


class Repository(ABC):
    async def query_header(self, request, search):
        query = await self.params_list(request)
        queryable = {}
        if "_id" in search:
            queryable["_id"] = ObjectId(search["_id"])
            return queryable
        if "id" in search:
            queryable["id"] = search["id"]
            return queryable
        for i in query:
            value = request.headers.get(i)
            if i == '_id':
                queryable[i] = ObjectId(value)
            elif value:
                queryable[i] = value
        return queryable

    async def params_list(self, request):
        return request.headers.get("query").split() \
            if request.headers.get("query") is not None else []

    @abstractmethod
    def init_app(self):
        """Initialize the factory method"""
        raise NotImplemented
