import json

from bson import ObjectId
from fastapi import HTTPException

from interfaces.repository_interface import RepositoryInterface


class RepositoryNOSQL(RepositoryInterface):
    def __init__(self, app, repository, access_point="/repository"):
        self.init_app(app, repository, access_point)

    def init_app(self, app, repository, access_point="/repository"):
        @app.get(access_point + "/{database_name}", tags=[access_point])
        async def read_all(database_name: str):
            table = repository[database_name]
            result = list(table.find())
            return json.dumps(result, default=str)

        @app.get(access_point + "/{database_name}/{item_code}", tags=[access_point])
        async def read_one(database_name: str, item_code: str):
            table = repository[database_name]
            result = list(table.find({"_id": ObjectId(item_code)}))
            if len(result) > 0:
                return json.dumps(result, default=str)
            else:
                raise HTTPException(status_code=404, detail="Item not found")


    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
