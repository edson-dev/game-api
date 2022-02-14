#python -m poetry export -f requirements.txt --output /application/requirements.txt
import mongoengine as mongoengine
from fastapi import FastAPI, Depends
import uvicorn
import psycopg2

from routes.crud.sql import SQL
from routes.crud.nosql import NoSQL
from routes.currency import router as router_currency
from routes.crypto import router as router_crypto
from routes.blockchain import router as router_blockchain
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import Response
from starlette.requests import Request

from dependencies import query_token, header_token


import dataset
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
template = Jinja2Templates(directory="./templates")
template.env.block_start_string = "[%"
template.env.block_end_string = "%]"
template.env.variable_start_string = "[["
template.env.variable_end_string = "]]"

env_psql = os.getenv("POSTGRESQL")
env_nosql = os.getenv("MONGODB")
database_postgres = dataset.connect(env_psql) #if env_psql else print("no database")
database_mongodb = mongoengine.connect(host=env_nosql, maxPoolSize=50) if env_nosql else print("no database")
#RepositorySQL(app, database_postgres, 'crud-sql')
SQL(app, database_postgres, 'crud-sql')
NoSQL(app, database_mongodb.database, 'crud-nosql')
#RepositoryNOSQL(app, database_mongodb.database, 'crud-nosql')

app.include_router(router_currency, prefix='/currency', tags=['currency'])
app.include_router(router_crypto, prefix='/crypto', tags=['crypto'])
app.include_router(router_blockchain, prefix='/blockchain', tags=['blockchain'])

@app.on_event("startup")
async def startup():
    ...

@app.on_event("shutdown")
async def shutdown():
    database_postgres.close()
    database_mongodb.close()


@app.get("/test", tags=["/test"])
def read_root():
    return {"response": "Hello World"}

@app.get("/cv", tags=["main"], response_class=HTMLResponse)
async def index(request: Request):
    data = {}
    print(f"data-load-page:{data}")
    return template.TemplateResponse("index.html", {"request": request,
                                                     "data_link": ['http://127.0.0.1:8080/index-data','http://127.0.0.1:8080/index-data2']})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, lifespan='on', reload=True)
