from fastapi import UploadFile, File, Request, Body, APIRouter, FastAPI, HTTPException
from typing import Optional, Dict
import json
from bson import json_util, ObjectId
from pymongo import database, collection
from routes.interfaces.crud import CRUD


class NoSQL(CRUD):
    def __init__(self, app: FastAPI, repository: collection.Collection, access_point="crud", dependencies=None):
        self.router = APIRouter()
        self.repository = repository
        self.init_app(self.router)
        app.include_router(prefix=f"/{access_point}",
                           router=self.router,
                           tags=[access_point],
                           dependencies=dependencies)

    def init_app(self, router):
        @router.post("/{collection_name}")
        async def create(collection_name: str, item: Dict[str, str], request: Request):
            table = self.repository[collection_name]
            items = await request.json()
            id = table.insert(items)
            return {
                "success": True,
                "data": json.loads(json.dumps(list(table.find({"_id": ObjectId(id)})), default=str))
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
            query = dict(await self.query_header(request, {}))
            values = await request.json()
            try:
                result = table.update(query, values)
                return {"success": True} if result['nModified'] > 0 else {"success": False}
            except Exception as e:
                raise HTTPException(status_code=409, detail={
                    "success": False,
                    "error": str(e),
                    "type": "Conflict"
                })

        @router.delete("/{collection_name}")
        async def delete(collection_name: str, request: Request, id: Optional[str] = None, skip: Optional[int] = 0, limit: Optional[int] = 100):
            table = self.repository[collection_name]
            query = await self.query_header(request, {"_id": id} if id is not None else {})
            result = table.delete_many(query)
            return {"success": True} \
                if result.acknowledged and result.deleted_count > 0 \
                else {"success": False}
