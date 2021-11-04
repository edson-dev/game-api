#python -m poetry export -f requirements.txt --output /application/requirements.txt
import mongoengine as mongoengine
import pymongo as pymongo
from mongoengine import connect
from fastapi import FastAPI
import uvicorn

from routes.repository.repository_nosql import RepositoryNOSQL
from routes.repository.repository_sql import RepositorySQL


import dataset
import os

app = FastAPI()

env_psql = os.getenv("POSTGRESQL")
env_nosql = os.getenv("MONGODB")
database_postgres = dataset.connect(env_psql) #if env_psql else print("no database")
database_mongodb = mongoengine.connect(host=env_nosql, maxPoolSize=50) if env_nosql else print("no database")
endpoints = {
    "api_psql": "api-psql",
    "api_nosql": "api-nosql"
}
RepositorySQL(app, database_postgres, f"/{endpoints['api_psql']}")
RepositoryNOSQL(app, database_mongodb.database, f"/{endpoints['api_nosql']}")


db = database_mongodb
@app.get("/test", tags=["/test"])
def read_root():
    return {"response": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
