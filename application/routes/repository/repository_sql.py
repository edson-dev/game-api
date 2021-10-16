from fastapi import HTTPException

from interfaces.repository_interface import RepositoryInterface
from fastapi import UploadFile, File, Request, Body


class RepositorySQL(RepositoryInterface):
    """
    :type repository: dataset database to connect
    """
    def __init__(self, app, repository, access_point="/repository"):
        self.init_app(app, repository, access_point)

    def init_app(self, app, repository, access_point="/repository"):
        self.create(app, repository, access_point)
        self.read(app, repository, access_point)
        self.update(app, repository, access_point)
        self.delete(app, repository, access_point)

    def create(self, app, repository, access_point="/repository"):
        @app.post(access_point + "/{name}", tags=[access_point])
        async def insert_itens(name: str, request: Request, payload: dict = Body(...)):
            table = repository[name]
            try:
                value = await request.json()
                if value[0]["id"]:
                    items = list(value)
                else:
                    items = [value]
                table.insert_many([ob for ob in items])
            except:
                ...
            return list(table.all())

    def read(self, app, repository, access_point):
        @app.get(access_point + "/{database_name}", tags=[access_point])
        async def get_all(database_name: str):
            table = repository[database_name]
            return list(table.all())

        @app.get(access_point + "/{database_name}/{item_code}", tags=[access_point])
        async def get_one(database_name: str, item_code: int):
            table = repository[database_name]
            result = list(table.find(id=item_code))
            if len(result) > 0:
                return result
            else:
                raise HTTPException(status_code=404, detail="Item not found")

    def update(self, app, repository, access_point):
        @app.put(access_point + "/{name}", tags=[access_point])
        async def upsert_itens(name: str, request: Request):
            table = repository[name]
            table.update(dict(await request.json()), ['id'])
            return list(table.all())

    def delete(self, app, repository, access_point):
        @app.delete(access_point + "/{name}", tags=[access_point])
        async def delete_itens(name: str, request: Request):
            table = repository[name]
            clause = dict(await request.json())
            table.delete(id=clause['id'])
            return list(table.all())
