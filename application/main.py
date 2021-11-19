#python -m poetry export -f requirements.txt --output /application/requirements.txt
import mongoengine as mongoengine
import pymongo as pymongo
from mongoengine import connect
from fastapi import FastAPI, Depends
import uvicorn

from routes.repository.sql import SQL
from routes.repository.nosql import NoSQL
from dependencies import query_token, header_token


import dataset
import os

app = FastAPI()

env_psql = os.getenv("POSTGRESQL")
env_nosql = os.getenv("MONGODB")
database_postgres = dataset.connect(env_psql) #if env_psql else print("no database")
database_mongodb = mongoengine.connect(host=env_nosql, maxPoolSize=50) if env_nosql else print("no database")
#RepositorySQL(app, database_postgres, 'api-sql')
SQL(app, database_postgres, '/api-sql')
NoSQL(app, database_mongodb.database, '/api-nosql')
#RepositoryNOSQL(app, database_mongodb.database, 'api-nosql')


db = database_mongodb
@app.get("/test", tags=["/test"])
def read_root():
    return {"response": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
