from dataset import Database
from fastapi import HTTPException

from interfaces.repository_interface import RepositoryInterface
from fastapi import UploadFile, File, Request, Body


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
        async def create(database_name: str, request: Request, payload: dict = Body(...)):
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
        async def read_all(database_name: str, request: Request):
            table = repository[database_name]
            query = await self.query_header(request)
            return list(table.find(**query))

        @app.get(access_point + "/{database_name}/{item_code}", tags=[access_point])
        async def read_one(database_name: str, item_code: int):
            table = repository[database_name]
            result = list(table.find(id=item_code))
            return result

    def update(self, app, repository, access_point):
        @app.put(access_point + "/{database_name}", tags=[access_point])
        async def upsert(database_name: str, request: Request):
            table = repository[database_name]
            table.update(dict(await request.json()), ['id'])
            return list(table.all())

    def delete(self, app, repository, access_point):
        @app.delete(access_point + "/{database_name}/{item_code}", tags=[access_point])
        async def delete(database_name: str, request: Request, item_code: int):
            table = repository[database_name]
            clause = dict(await request.json())
            table.delete(id=clause['id'])
            return list(table.all())
