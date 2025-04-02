from httpx import AsyncClient


async def test_root(client: AsyncClient):
    response = await client.get("/")

    assert response.status_code == 200
    assert "Pottato" in response.text


async def test_run_code(client: AsyncClient):
    test_code = "1 + 1"

    response = await client.post("/run-code", json={"code": test_code})

    assert response.json() == {"result": "2"}


async def test_get_files(client: AsyncClient):
    response = await client.get("/files")

    assert response.json() == {"files": []}
