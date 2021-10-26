import json
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

    def create(self, app, repository, access_point):
        pass

    def read(self, app, repository, access_point):
        @app.get(access_point + "/{database_name}", tags=[access_point])
        async def read_all(database_name: str, request: Request, skip: Optional[int] = 0, limit: Optional[int] = 100):
            table = repository[database_name]
            list_params = request.headers.raw
            query = {}
            for i in list_params:
                key = i[0].decode()
                if key not in ["connection","accept-encoding","accept","user-agent","host","content-length","content-type","postman-token"]:
                    if type(i[1].decode()) == dict:
                        value = json.loads(i[1].decode())
                    elif i[1].decode() == "True" or i[1].decode() == "False":
                        value = True if i[1].decode() == "True" else False
                    else:
                        try:
                            value = float(i[1].decode())
                        except:
                            value = i[1].decode()
                    query[key] = value
            result = list(table.find(query))
            return json.dumps(result[skip:skip+limit], default=str)

        @app.get(access_point + "/{database_name}/{item_code}", tags=[access_point])
        async def read_one(database_name: str, item_code: str):
            table = repository[database_name]
            result = list(table.find_one({"_id": ObjectId(item_code)}))
            if len(result) > 0:
                return json.dumps(result, default=str)
            else:
                raise HTTPException(status_code=404, detail="Item not found")

    def update(self, app, repository, access_point):
        pass

    def delete(self, app, repository, access_point):
        pass
