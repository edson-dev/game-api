from fastapi import UploadFile, File, Request, Body, APIRouter, FastAPI, Response
from typing import Optional, Dict, List
import json
from bson import json_util, ObjectId


from controllers.data import *
from routes.interfaces.crud import CRUD


class SQL(CRUD):
    def __init__(self, app: FastAPI, repository, access_point="crud", dependencies=None):
        self.router = APIRouter()
        self.repository = repository
        self.init_app(self.router)
        app.include_router(prefix=f"/{access_point}",
                           router=self.router,
                           tags=[access_point],
                           dependencies=dependencies)

    def init_app(self, router):
        @router.post("/{table_name}")
        async def create(table_name: str, item: List[Dict[str, str]], request: Request, resp: Response):
            table = self.repository[table_name]
            items = await request.json()
            try:
                if isinstance(items, list):
                    result = []
                    for ob in list(items):
                        result.append(table.insert(ob))
                else:
                    result = table.insert(items)
                return response(result)
            except Exception as e:
                resp.status_code = 409
                return response(ResponseError(status_code=409, fields={
                    "status": "fail",
                    "error": str(e),
                    "type": "Conflict"
                }))

        @router.get("/{table_name}")
        async def read(request: Request, table_name: Optional[str] = "test", id: Optional[int] = None, skip: Optional[int] = 0, limit: Optional[int] = 100):
            table = self.repository[table_name]
            query = await self.query_header(request, {"id": id} if id is not None else {})
            result = list(table.find(**query))
            return response(result, skip, limit)

        @router.put("/{table_name}")
        async def upsert(table_name: str, request: Request):
            table = self.repository[table_name]
            keys = await self.params_list(request)
            values = dict(await request.json())
            try:
                table.upsert(values, keys)
                return response(list(table.all()))
            except Exception as e:
                response(ResponseError(status_code=409, fields={
                    "status": "fail",
                    "error": str(e),
                    "type": "Conflict"
                }))

        @router.delete("/{table_name}")
        async def delete(table_name: str, request: Request):
            table = self.repository[table_name]
            query = await self.query_header(request, {})
            if query:
                if 'all' in query.keys():
                    query = {}
                table.delete(**query)
            return response(list(table.all()))
