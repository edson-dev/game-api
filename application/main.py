#python -m poetry export -f requirements.txt --output /application/requirements.txt
from fastapi import FastAPI
import uvicorn

from routes.repository.repository_nosql import RepositoryNOSQL
from routes.repository.repository_sql import RepositorySQL
from routes.repository import api

import dataset
import os

app = FastAPI()

#api.init_app(app, "/api")
postgres_database = dataset.connect(os.getenv("POSTGRESQL"))
RepositorySQL(app, postgres_database, "/api-psql")
RepositoryNOSQL(app, "/api-nosql")

@app.get("/test", tags=["/test"])
def read_root():
    return {"response": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
