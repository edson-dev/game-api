from fastapi import UploadFile, File, Request, Body, APIRouter, FastAPI, HTTPException
from typing import Optional
import json
from bson import json_util, ObjectId

from routes.interfaces.repository import Repository


class SQL(Repository):
    def __init__(self, app: FastAPI, repository, access_point="/repository", dependencies=None):
        self.router = APIRouter()
        self.repository = repository
        self.init_app(self.router)
        app.include_router(prefix=access_point,
                           router=self.router,
                           tags=[access_point],
                           dependencies=dependencies)

    def init_app(self, router):
        @router.post("/{table_name}")
        async def create(table_name: str, request: Request):
            table = self.repository[table_name]
            items = await request.json()
            if isinstance(items, list):
                table.insert_many([ob for ob in list(items)])
            else:
                table.insert(items)
            return {
                "success": True,
                "data": list(table.all())
            }

        @router.get("/{table_name}")
        async def read(request: Request, table_name: Optional[str] = "test", id: Optional[int] = None, skip: Optional[int] = 0, limit: Optional[int] = 100):
            table = self.repository[table_name]
            query = await self.query_header(request, {"id": id} if id is not None else {})
            result = list(table.find(**query))
            return json.loads(json_util.dumps(result[skip:skip + limit]))

        @router.put("/{table_name}")
        async def upsert(table_name: str, request: Request):
            table = self.repository[table_name]
            keys = await self.params_list(request)
            values = dict(await request.json())
            try:
                table.upsert(values, keys)
                return list(table.all())
            except Exception as e:
                raise HTTPException(status_code=409, detail={
                    "success": False,
                    "error": str(e),
                    "type": "Conflict"
                })

        @router.delete("/{table_name}")
        async def delete(table_name: str, request: Request):
            table = self.repository[table_name]
            query = await self.query_header(request, {})
            if query:
                if 'all' in query.keys():
                    query = {}
                table.delete(**query)
            return list(table.all())
