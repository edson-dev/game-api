from base_test import *

@pytest.mark.anyio
async def test_create():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post("crud-sql/test",
                                     json={"name": "test",
                                           "status": "created"})
    assert response.status_code == 200
    assert True == response.json()["success"]

@pytest.mark.anyio
async def test_read():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get('crud-sql/test',
                                headers={"query": "name",
                                         "name": "test"})
    assert response.status_code == 200

@pytest.mark.anyio
async def test_update():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.put("crud-sql/test",
                    headers={"query": "name", "name": "test"},
                    json={
                        "status": "update",
                        "name": "test"
                    })
    assert response.status_code == 200

@pytest.mark.anyio
async def test_delete():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.delete('crud-sql/test',
                                   headers={"query": "name", "name": "test"}
                                   )
    assert response.status_code == 200