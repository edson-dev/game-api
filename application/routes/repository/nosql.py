from fastapi import UploadFile, File, Request, Body, APIRouter, FastAPI, HTTPException
from typing import Optional
import json
from bson import json_util, ObjectId

from routes.interfaces.repository import Repository


class NoSQL(Repository):
    def __init__(self, app: FastAPI, repository, access_point="/repository", dependencies=None):
        self.router = APIRouter()
        self.repository = repository
        self.init_app(self.router)
        app.include_router(prefix=access_point,
                           router=self.router,
                           tags=[access_point],
                           dependencies=dependencies)

    def init_app(self, router):
        @router.post("/{collection_name}")
        async def create(collection_name: str, request: Request):
            table = self.repository[collection_name]
            items = await request.json()
            item = table.insert(items)
            return {
                "success": True,
                "data": json.loads(json.dumps(list(table.find({"_id": ObjectId(item)})), default=str))
            }

        @router.get("/{collection_name}")
        async def read(collection_name: str, request: Request, id: Optional[str] = None, skip: Optional[int] = 0, limit: Optional[int] = 100):
            table = self.repository[collection_name]
            query = await self.query_header(request, {"_id": id} if id is not None else {})
            result = list(table.find(query))
            return json.loads(json.dumps(result[skip:skip + limit], default=str))

        @router.put("/{collection_name}")
        async def upsert(collection_name: str, request: Request):
            table = self.repository[collection_name]
            keys = await self.params_list(request)
            values = dict(await self.query_header(request))
            try:
                result = table.upsert(values, keys)
                return list(result)
            except Exception as e:
                raise HTTPException(status_code=409, detail={
                    "success": False,
                    "error": str(e),
                    "type": "Conflict"
                })

        @router.delete("/{collection_name}")
        async def delete(collection_name: str, request: Request):
            table = self.repository[collection_name]
            query = await self.query_header(request)
            ...
