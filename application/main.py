#python -m poetry export -f requirements.txt --output /application/requirements.txt
from fastapi import FastAPI, Depends
import uvicorn

from routes.crud.lake import Lake
from routes.currency import router as router_currency
from routes.crypto import router as router_crypto
from routes.blockchain import router as router_blockchain
from fastapi.staticfiles import StaticFiles
import asyncio
from routes.bot import Bot


from dependencies import query_token, header_token


import dataset
import os
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
env_psql = os.getenv("POSTGRESQL")
#env_nosql = os.getenv("MONGODB")
database_postgres = dataset.connect(env_psql) #if env_psql else print("no database")
#database_mongodb = mongoengine.connect(host=env_nosql, maxPoolSize=50) if env_nosql else print("no database")
#RepositorySQL(app, database_postgres, 'crud-sql')
#SQL(app, database_postgres, 'crud-sql')
#NoSQL(app, database_mongodb.database, 'crud-nosql')
#RepositoryNOSQL(app, database_mongodb.database, 'crud-nosql')
Lake(app,'','lake')
app.include_router(router_currency, prefix='/currency', tags=['currency'])
app.include_router(router_crypto, prefix='/crypto', tags=['crypto'])
app.include_router(router_blockchain, prefix='/blockchain', tags=['blockchain'])




@app.on_event("startup")
async def startup():
    #asyncio.create_task(Bot().start(os.getenv("BOT_TOKEN")))
    ...

@app.on_event("shutdown")
async def shutdown():
    database_postgres.close()
    #database_mongodb.close()


@app.get("/", tags=["/test"])
def read_root():
    return {"response": "Hello World"}

@app.get("/healthcheck")
def read_root():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, lifespan='on', reload=True)
