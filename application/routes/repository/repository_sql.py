from fastapi import HTTPException

from interfaces.repository_interface import RepositoryInterface


class RepositorySQL(RepositoryInterface):
    """
    :type repository: dataset database to connect
    """
    def __init__(self, app, repository, access_point="/repository"):
        self.init_app(app, repository, access_point)

    def init_app(self, app, repository, access_point="/repository"):
        self.read(app, repository, access_point)

    def create(self):
        pass

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

    def update(self):
        pass

    def delete(self):
        pass
