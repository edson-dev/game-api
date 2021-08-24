from fastapi import FastAPI
import uvicorn
from routes import api

app = FastAPI()

api.init_app(app,"/api")


@app.get("/", tags=["/view"])
def read_root():
    return "test"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
