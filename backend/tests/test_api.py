import pytest
from httpx import AsyncClient, ASGITransport
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

sys.path.append(os.path.abspath('../src'))

from app import app

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture(autouse=True)
async def clear_db(anyio_backend):
    load_dotenv()
    client = AsyncIOMotorClient(os.getenv('DB_URL'))
    db = client[os.getenv('TEST_DB_NAME')]
    collections = await db.list_collection_names()

    # Drop each collection
    for collection_name in collections:
        await db.drop_collection(collection_name)
        print(f"Dropped collection: {collection_name}")

    # Optionally, close the client connection
    client.close()

@pytest.mark.anyio
async def test_read_main(clear_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.anyio
async def test_read_projects(clear_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/projects")
    assert response.status_code == 200
    assert response.json() == []
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/projects/",
                          json = {"id" : "0", "name": "test", "description" : "For testing"}
                          )
    assert response.status_code == 200