from base_test import *


@pytest.mark.anyio
async def test_create():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post("crud-nosql/test",
                                 json={"name": "test"})
    assert response.status_code == 200


@pytest.mark.anyio
async def test_read():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get("crud-nosql/test",
                                headers={"query": "name status",
                                         "name": "test"})
    assert response.status_code == 200
