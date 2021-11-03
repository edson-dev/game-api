from ..base_test import *

@pytest.mark.anyio
async def test_create():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post(f"{endpoints['api_psql']}/test",
                                     json={"name": "test1"})
    assert response.status_code == 200
    assert True == response.json()["success"]

@pytest.mark.anyio
async def test_read():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(f"{endpoints['api_psql']}/test",
                                headers={"query": "name status",
                                         "name": "test"})
    assert response.status_code == 200
