import json
from bson import json_util
from typing import Optional
import itertools
import numbers
from distutils.util import strtobool
from bson import ObjectId
from fastapi import HTTPException, Query, Request
from pymongo.database import Database


from interfaces.repository_interface import RepositoryInterface


class RepositoryNOSQL(RepositoryInterface):

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
            item = table.insert(items)
            return {
                "success": True,
                "data": json.loads(json_util.dumps(table.find({"_id": ObjectId(item)})))
            }

    def read(self, app, repository: Database, access_point):
        @app.get(access_point + "/{database_name}", tags=[access_point])
        async def read(database_name: str, request: Request, skip: Optional[int] = 0, limit: Optional[int] = 100):
            table = repository[database_name]
            query = await self.query_header(request)
            result = list(table.find({}))
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
        pass
