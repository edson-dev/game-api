#python -m poetry export -f requirements.txt --output /application/requirements.txt
import mongoengine as mongoengine
import pymongo as pymongo
from mongoengine import connect
from fastapi import FastAPI
import uvicorn

from routes.repository.repository_nosql import RepositoryNOSQL
from routes.repository.repository_sql import RepositorySQL
from routes.repository import api

import dataset
import os

app = FastAPI()

#api.init_app(app, "/api")
database_postgres = dataset.connect(os.getenv("POSTGRESQL"))
database_mongodb = mongoengine.connect(host=os.getenv("MONGODB_URL")).database

RepositorySQL(app, database_postgres, "/api-psql")
RepositoryNOSQL(app, database_mongodb, "/api-nosql")


db = database_mongodb
@app.get("/test", tags=["/test"])
def read_root():
    return {"response": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
