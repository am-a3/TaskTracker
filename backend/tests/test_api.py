import pytest
from httpx import AsyncClient, ASGITransport
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
sys.path.append(os.path.abspath('../src'))
from app import app
import pytest_asyncio

pytestmark = pytest.mark.asyncio(scope="module")

__test_project_1 = {"id" : "0", "name": "test", "description" : "For testing"}
__test_project_2 = {"id" : "0", "name": "test 2", "description" : "For testing 2"}
__test_project_3 = {"id" : "0", "name": "test 3", "description" : "For testing 3"}

def __compare_dict_without_id(test: dict, reference: dict, exclude: list[str]) -> bool:
    for key in reference:
        if key in exclude:
            continue

        if key in test:
            if test[key] != reference[key]:
                return False
        else:
            return False
        
    return True

#@pytest_asyncio.fixture(scope="module")
async def clear_db():
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
    return True

async def test_read_main():
    await clear_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

async def test_read_write_projects():
    await clear_db()
    # test no projects:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/projects")
    assert response.status_code == 200
    assert response.json() == []
    
    # test one project:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/projects/",
                          json = __test_project_1
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/projects/{__id}")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json(), __test_project_1, ["id", "description"])

    #test multiple projects:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/projects/",
                          json = __test_project_2
                          )
    assert response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/projects")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json()[0], __test_project_1, ["id", "description"])
    assert __compare_dict_without_id(response.json()[1], __test_project_2, ["id", "description"])

async def test_delete_projects():
    await clear_db()
    #add project:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/projects/",
                          json = __test_project_3
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    #check that it has been added:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/projects/{__id}")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json(), __test_project_3, ["id", "description"])

    #delete project:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete(f"/projects/{__id}")
    assert response.status_code == 200

    #check that project has been removed:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/projects")
    assert response.status_code == 200
    assert response.json() == []