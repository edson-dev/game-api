#python -m poetry export -f requirements.txt --output /application/requirements.txt
import mongoengine as mongoengine
from fastapi import FastAPI, Depends
import uvicorn

from routes.crud.sql import SQL
from routes.crud.nosql import NoSQL
from routes.currency import Currency
from dependencies import query_token, header_token


import dataset
import os

app = FastAPI()

env_psql = os.getenv("POSTGRESQL")
env_nosql = os.getenv("MONGODB")
database_postgres = dataset.connect(env_psql) #if env_psql else print("no database")
database_mongodb = mongoengine.connect(host=env_nosql, maxPoolSize=50) if env_nosql else print("no database")
#RepositorySQL(app, database_postgres, 'crud-sql')
SQL(app, database_postgres, '/crud-sql')
NoSQL(app, database_mongodb.database, '/crud-nosql')
Currency(app, database_postgres, '/currency')
#RepositoryNOSQL(app, database_mongodb.database, 'crud-nosql')


@app.on_event("startup")
async def startup():
    ...

@app.on_event("shutdown")
async def shutdown():
    database_postgres.close()
    database_mongodb.close()


@app.get("/test", tags=["/test"])
def read_root():
    return {"response": "Hello Worlds"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, lifespan='on', reload=True)
