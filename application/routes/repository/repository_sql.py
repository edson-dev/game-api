from dataset import Database
from fastapi import HTTPException

from interfaces.repository_interface import RepositoryInterface
from fastapi import UploadFile, File, Request, Body
from typing import Optional
import json
from bson import json_util

class RepositorySQL(RepositoryInterface):
    def __init__(self, app, repository: Database, access_point="/repository"):
        self.init_app(app, repository, access_point)

    def init_app(self, app, repository, access_point="/repository"):
        self.create(app, repository, access_point)
        self.read(app, repository, access_point)
        self.update(app, repository, access_point)
        self.delete(app, repository, access_point)

    def create(self, app, repository: Database, access_point):
        @app.post(access_point + "/{database_name}", tags=[access_point])
        async def create(database_name: str, request: Request):
            table = repository[database_name]
            items = await request.json()
            if isinstance(items, list):
                table.insert_many([ob for ob in list(items)])
            else:
                table.insert(items)
            return {
                    "success": True,
                    "data": list(table.all())
            }

    def read(self, app, repository, access_point):
        @app.get(access_point + "/{database_name}", tags=[access_point])
        async def read(database_name: str, request: Request, skip: Optional[int] = 0, limit: Optional[int] = 100):
            table = repository[database_name]
            query = await self.query_header(request)
            result = list(table.find(**query))
            return json.loads(json_util.dumps(result[skip:skip+limit]))

    def update(self, app, repository, access_point):
        @app.put(access_point + "/{database_name}", tags=[access_point])
        async def upsert(database_name: str, request: Request):
            table = repository[database_name]
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

    def delete(self, app, repository, access_point):
        @app.delete(access_point + "/{database_name}", tags=[access_point])
        async def delete(database_name: str, request: Request):
            table = repository[database_name]
            query = await self.query_header(request)
            if query:
                if 'all' in query.keys():
                    query = {}
                table.delete(**query)
            return list(table.all())
