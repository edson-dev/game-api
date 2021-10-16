#python -m pytest -W ignore::DeprecationWarning
from fastapi.testclient import TestClient

import sys


sys.path.append("../application")
from main import app
import nest_asyncio
nest_asyncio.apply()

client = TestClient(app)


async def test_read_test():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World"}
