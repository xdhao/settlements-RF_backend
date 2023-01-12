import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from modules.excel_data_module.main import app

client = TestClient(app)


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_read_countries():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/excel-data/v1.0/get-counties")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_read_federals():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/excel-data/v1.0/get-federal-districts")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_read_aut_districts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/excel-data/v1.0/get-autonomic-districts")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_read_regions():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/excel-data/v1.0/get-regions/bc7753ab-f8fc-4769-8d49-dbe4708d32b0")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_read_cities():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/excel-data/v1.0/get-local-objects/9df08d1e-38c2-4164-acff-251d8b400002")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_read_analitic_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/excel-data/v1.0/get-perc-urbal-rural")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_read_analitic_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/excel-data/v1.0/get-medium-value-of-subject-types")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_read_analitic_3():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/excel-data/v1.0/get-medium-people-perc")

    assert response.status_code == 200