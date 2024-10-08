import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os
sys.path.append(os.path.abspath('../src'))
sys.path.append(os.path.abspath('.'))
from app import app
from common_utils import compare_dict_without_id, clear_db, test_project_1, test_project_2, test_project_3,\
                            test_location_1, test_location_2, test_location_3, test_task_1, test_task_2, test_task_3,\
                            test_task_done, test_task_not_done, \
                            test_tag_1, test_tag_2, test_tag_3, NOT_VALID_ID

BASE_URL = "http://test/v1"

pytestmark = pytest.mark.asyncio(scope="module")

async def test_read_main():
    await clear_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

async def test_read_write_projects():
    await clear_db()
    # test no projects:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/projects")
    assert response.status_code == 200
    assert response.json() == []
    
    # test not valid id:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/projects/{NOT_VALID_ID}")
    assert response.status_code == 400

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.delete(f"/projects/{NOT_VALID_ID}")
    assert response.status_code == 400

    # test one project:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/projects/",
                          json = test_project_1
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/projects/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), test_project_1, ["id", "description"])

    #test multiple projects:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/projects/",
                          json = test_project_2
                          )
    assert response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/projects")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json()[0], test_project_1, ["id", "description"])
    assert compare_dict_without_id(response.json()[1], test_project_2, ["id", "description"])

async def test_update_project():
    await clear_db()
    #add project:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/projects/",
                          json = test_project_3
                          )
    
    assert response.status_code == 200
    __id = response.json()["id"]

    #update project:
    modified_entry = test_project_3
    modified_entry["id"] = __id
    modified_entry["name"] = "Modified"

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.put(f"/projects/{__id}",
                          json = modified_entry
                          )
        
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), modified_entry, ["id"])

    #readback project:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/projects/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), modified_entry, ["id"])

async def test_delete_projects():
    await clear_db()
    #add project:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/projects/",
                          json = test_project_3
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    #check that it has been added:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/projects/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), test_project_3, ["id", "description"])

    #delete project:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.delete(f"/projects/{__id}")
    assert response.status_code == 200

    #check that project has been removed:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/projects")
    assert response.status_code == 200
    assert response.json() == []

async def test_read_write_locations():
    await clear_db()

    # test not valid id:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/locations/{NOT_VALID_ID}")
    assert response.status_code == 400

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.delete(f"/locations/{NOT_VALID_ID}")
    assert response.status_code == 400

    # test no locations:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/locations")
    assert response.status_code == 200
    assert response.json() == []

    # test one location:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/locations/",
                          json = test_location_1
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/locations/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), test_location_1, ["id", "description"])

    #test multiple locations:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/locations/",
                          json = test_location_2
                          )
    assert response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/locations")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json()[0], test_location_1, ["id", "description"])
    assert compare_dict_without_id(response.json()[1], test_location_2, ["id", "description"])

async def test_update_location():
    await clear_db()
    #add location:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/locations/",
                          json = test_location_3
                          )
    
    assert response.status_code == 200
    __id = response.json()["id"]

    #update location:
    modified_entry = test_location_3
    modified_entry["id"] = __id
    modified_entry["name"] = "Modified"

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.put(f"/locations/{__id}",
                          json = modified_entry
                          )
        
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), modified_entry, ["id"])

    #readback location:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/locations/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), modified_entry, ["id"])

async def test_delete_locations():
    await clear_db()
    #add location:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/locations/",
                          json = test_location_3
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    #check that it has been added:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/locations/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), test_location_3, ["id", "description"])

    #delete location:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.delete(f"/locations/{__id}")
    assert response.status_code == 200

    #check that location has been removed:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/locations")
    assert response.status_code == 200
    assert response.json() == []

async def test_read_write_tasks():
    await clear_db()

    # test not valid id:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/tasks/{NOT_VALID_ID}")
    assert response.status_code == 400

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.delete(f"/tasks/{NOT_VALID_ID}")
    assert response.status_code == 400

    # test no tasks:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

    # test one task:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tasks/",
                          json = test_task_1
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/tasks/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), test_task_1, ["id", "description"])

    #test multiple tasks:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tasks/",
                          json = test_task_2
                          )
    assert response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/tasks")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json()[0], test_task_1, ["id", "description"])
    assert compare_dict_without_id(response.json()[1], test_task_2, ["id", "description"])

async def test_update_task():
    await clear_db()
    #add task:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tasks/",
                          json = test_task_3
                          )
    
    assert response.status_code == 200
    __id = response.json()["id"]

    #update task:
    modified_entry = test_task_3
    modified_entry["id"] = __id
    modified_entry["name"] = "Modified"

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.put(f"/tasks/{__id}",
                          json = modified_entry
                          )
        
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), modified_entry, ["id"])

    #readback task:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/tasks/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), modified_entry, ["id"])

async def test_delete_tasks():
    await clear_db()
    #add task:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tasks/",
                          json = test_task_3
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    #check that it has been added:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/tasks/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), test_task_3, ["id", "description"])

    #delete task:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.delete(f"/tasks/{__id}")
    assert response.status_code == 200

    #check that task has been removed:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

async def test_task_done_requests():
    await clear_db()
    #add tasks:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tasks/",
                          json = test_task_done
                          )
    assert response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tasks/",
                          json = test_task_not_done
                          )
    assert response.status_code == 200

    # check done task request:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/tasks/done")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert compare_dict_without_id(response.json()[0], test_task_done, ["id", "description"])

    # check not done task request:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/tasks/not_done")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert compare_dict_without_id(response.json()[0], test_task_not_done, ["id", "description"])

async def test_read_write_tags():
    await clear_db()

    # test not valid id:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/tags/{NOT_VALID_ID}")
    assert response.status_code == 400

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.delete(f"/tags/{NOT_VALID_ID}")
    assert response.status_code == 400

    # test no tags:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/tags")
    assert response.status_code == 200
    assert response.json() == []

    # test one tag:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tags/",
                          json = test_tag_1
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/tags/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), test_tag_1, ["id", "description"])

    #test multiple tags:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tags/",
                          json = test_tag_2
                          )
    assert response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/tags")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json()[0], test_tag_1, ["id", "description"])
    assert compare_dict_without_id(response.json()[1], test_tag_2, ["id", "description"])

async def test_update_tag():
    await clear_db()
    #add tag:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tags/",
                          json = test_tag_3
                          )
    
    assert response.status_code == 200
    __id = response.json()["id"]

    #update tag:
    modified_entry = test_tag_3
    modified_entry["id"] = __id
    modified_entry["name"] = "Modified"

    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.put(f"/tags/{__id}",
                          json = modified_entry
                          )
        
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), modified_entry, ["id"])

    #readback task:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/tags/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), modified_entry, ["id"])

async def test_delete_tags():
    await clear_db()
    #add tag:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/tags/",
                          json = test_tag_3
                          )
    assert response.status_code == 200
    __id = response.json()["id"]

    #check that it has been added:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get(f"/tags/{__id}")
    assert response.status_code == 200
    assert compare_dict_without_id(response.json(), test_tag_3, ["id", "description"])

    #delete tag:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.delete(f"/tags/{__id}")
    assert response.status_code == 200

    #check that tag has been removed:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/tags")
    assert response.status_code == 200
    assert response.json() == []