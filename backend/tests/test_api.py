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

__test_project_1 = {"id" : "0", "name": "project test", "description" : "For testing"}
__test_project_2 = {"id" : "0", "name": "project test 2", "description" : "For testing 2"}
__test_project_3 = {"id" : "0", "name": "project test 3", "description" : "For testing 3"}

__test_location_1 = {"id" : "0", "name": "location test", "description" : "For testing"}
__test_location_2 = {"id" : "0", "name": "location test 2", "description" : "For testing 2"}
__test_location_3 = {"id" : "0", "name": "location test 3", "description" : "For testing 3"}

__test_task_1 = {"id" : "0", "name": "task test", "description" : "For testing"}
__test_task_2 = {"id" : "0", "name": "task test 2", "description" : "For testing 2"}
__test_task_3 = {"id" : "0", "name": "task test 3", "description" : "For testing 3"}

__test_tag_1 = {"id" : "0", "name": "tag test", "description" : "For testing"}
__test_tag_2 = {"id" : "0", "name": "tag test 2", "description" : "For testing 2"}
__test_tag_3 = {"id" : "0", "name": "tag test 3", "description" : "For testing 3"}

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

async def test_read_write_locations():
    await clear_db()

    # test no locations:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/locations")
    assert response.status_code == 200
    assert response.json() == []

    # test one location:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/locations/",
                          json = __test_location_1
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/locations/{__id}")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json(), __test_location_1, ["id", "description"])

    #test multiple locations:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/locations/",
                          json = __test_location_2
                          )
    assert response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/locations")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json()[0], __test_location_1, ["id", "description"])
    assert __compare_dict_without_id(response.json()[1], __test_location_2, ["id", "description"])

async def test_delete_locations():
    await clear_db()
    #add location:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/locations/",
                          json = __test_location_3
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    #check that it has been added:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/locations/{__id}")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json(), __test_location_3, ["id", "description"])

    #delete location:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete(f"/locations/{__id}")
    assert response.status_code == 200

    #check that location has been removed:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/locations")
    assert response.status_code == 200
    assert response.json() == []

async def test_read_write_tasks():
    await clear_db()

    # test no tasks:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

    # test one task:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/tasks/",
                          json = __test_task_1
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/tasks/{__id}")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json(), __test_task_1, ["id", "description"])

    #test multiple tasks:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/tasks/",
                          json = __test_task_2
                          )
    assert response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tasks")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json()[0], __test_task_1, ["id", "description"])
    assert __compare_dict_without_id(response.json()[1], __test_task_2, ["id", "description"])

async def test_delete_tasks():
    await clear_db()
    #add task:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/tasks/",
                          json = __test_task_3
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    #check that it has been added:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/tasks/{__id}")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json(), __test_task_3, ["id", "description"])

    #delete task:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete(f"/tasks/{__id}")
    assert response.status_code == 200

    #check that task has been removed:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

async def test_read_write_tags():
    await clear_db()

    # test no tags:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tags")
    assert response.status_code == 200
    assert response.json() == []

    # test one tag:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/tags/",
                          json = __test_tag_1
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/tags/{__id}")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json(), __test_tag_1, ["id", "description"])

    #test multiple tags:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/tags/",
                          json = __test_tag_2
                          )
    assert response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tags")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json()[0], __test_tag_1, ["id", "description"])
    assert __compare_dict_without_id(response.json()[1], __test_tag_2, ["id", "description"])

async def test_delete_tags():
    await clear_db()
    #add tag:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/tags/",
                          json = __test_tag_3
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    #check that it has been added:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/tags/{__id}")
    assert response.status_code == 200
    assert __compare_dict_without_id(response.json(), __test_tag_3, ["id", "description"])

    #delete tag:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete(f"/tags/{__id}")
    assert response.status_code == 200

    #check that tag has been removed:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tags")
    assert response.status_code == 200
    assert response.json() == []