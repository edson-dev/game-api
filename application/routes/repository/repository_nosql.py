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
            table.insert(items)
            return {
                "success": True,
                "data": table.find({})
            }

    def read(self, app, repository, access_point):
        @app.get(access_point + "/{database_name}", tags=[access_point])
        async def read_all(database_name: str, request: Request, skip: Optional[int] = 0, limit: Optional[int] = 100):
            table = repository[database_name]
            result = list(table.find(await self.query_header(request)))
            return json.loads(json_util.dumps(result[skip:skip+limit]))


        @app.get(access_point + "/{database_name}/{item_code}", tags=[access_point])
        async def read_one(database_name: str, item_code: str):
            table = repository[database_name]
            result = list(table.find_one({"_id": ObjectId(item_code)}))
            if len(result) == 1:
                return json.dumps(result, default=str)
            else:
                raise HTTPException(status_code=404, detail="Item not found")

    def update(self, app, repository, access_point):
        pass

    def delete(self, app, repository, access_point):
        pass
