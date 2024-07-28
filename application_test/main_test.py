#python -m pytest -W ignore::DeprecationWarning

from .base_test import *

client = TestClient(app)

async def test_read_sync():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World"}

@pytest.mark.anyio
async def test_read_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/test")
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World"}