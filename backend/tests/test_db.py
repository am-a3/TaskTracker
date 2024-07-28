import pytest
import sys
import os
from dotenv import load_dotenv
from ..src.mongodb_client import MongoDbClient
from common_utils import compare_dict_without_id, clear_db, test_project_1, test_project_2, test_project_3,\
                            test_location_1, test_location_2, test_location_3, test_task_1, test_task_2, test_task_3,\
                            test_tag_1, test_tag_2, test_tag_3

@pytest.fixture
async def create_db_client():
    load_dotenv(dotenv_path="../src/.env")
    print(f"{os.getenv('DB_URL')} {os.getenv('TEST_DB_NAME')}")
    client = MongoDbClient(os.getenv('DB_URL'), os.getenv('TEST_DB_NAME'))
    return client

async def test_project(create_db_client):
    await clear_db()
    client = create_db_client

    #test no projects:
    projects = await client.request_all_projects()
    assert projects == []

    #request non existing project:
    project = await client.request_project("11deadbeef2211deadbeef22")
    assert project == None

    #insert project 1:
    project_id = await client.insert_project(test_project_1)
    project = await client.request_project(project_id)
    assert compare_dict_without_id(project, test_project_1, ["id"])

    #insert project 2:
    project_id = await client.insert_project(test_project_2)
    project = await client.request_project(project_id)
    assert compare_dict_without_id(project, test_project_2, ["id"])

    #request all projects:
    projects = await client.request_all_projects()
    assert compare_dict_without_id(projects[0], test_project_1, ["id", "description"])
    assert compare_dict_without_id(projects[1], test_project_2, ["id", "description"])

    #delete project:
    project_id = await client.insert_project(test_project_3)
    project = await client.request_project(project_id)
    assert compare_dict_without_id(project, test_project_3, ["id"])
    result = await client.delete_project(project_id)
    assert result != None
    project = await client.request_project(project_id)
    assert project == None

async def test_location(create_db_client):
    await clear_db()
    client = create_db_client

    #test no location:
    locations = await client.request_all_locations()
    assert locations == []

    #request non existing location:
    location = await client.request_location("11deadbeef2211deadbeef22")
    assert location == None

    #insert location 1:
    location_id = await client.insert_location(test_location_1)
    location = await client.request_location(location_id)
    assert compare_dict_without_id(location, test_location_1, ["id"])

    #insert location 2:
    location_id = await client.insert_location(test_location_2)
    location = await client.request_location(location_id)
    assert compare_dict_without_id(location, test_location_2, ["id"])

    #request all locations:
    locations = await client.request_all_locations()
    assert compare_dict_without_id(locations[0], test_location_1, ["id", "description"])
    assert compare_dict_without_id(locations[1], test_location_2, ["id", "description"])

    #delete location:
    location_id = await client.insert_location(test_location_3)
    location = await client.request_location(location_id)
    assert compare_dict_without_id(location, test_location_3, ["id"])
    result = await client.delete_location(location_id)
    assert result != None
    location = await client.request_location(location_id)
    assert location == None

async def test_task(create_db_client):
    await clear_db()
    client = create_db_client

    #test no task:
    tasks = await client.request_all_tasks()
    assert tasks == []

    #request non existing task:
    task = await client.request_task("11deadbeef2211deadbeef22")
    assert task == None

    #insert task 1:
    task_id = await client.insert_task(test_task_1)
    task = await client.request_task(task_id)
    assert compare_dict_without_id(task, test_task_1, ["id"])

    #insert task 2:
    task_id = await client.insert_task(test_task_2)
    task = await client.request_task(task_id)
    assert compare_dict_without_id(task, test_task_2, ["id"])

    #request all tasks:
    tasks = await client.request_all_tasks()
    assert compare_dict_without_id(tasks[0], test_task_1, ["id", "description"])
    assert compare_dict_without_id(tasks[1], test_task_2, ["id", "description"])

    #delete task:
    task_id = await client.insert_task(test_task_3)
    task = await client.request_task(task_id)
    assert compare_dict_without_id(task, test_task_3, ["id"])
    result = await client.delete_task(task_id)
    assert result != None
    task = await client.request_task(task_id)
    assert task == None

async def test_tag(create_db_client):
    await clear_db()
    client = create_db_client

    #test no tag:
    tags = await client.request_all_tags()
    assert tags == []

    #request non existing tag:
    tag = await client.request_tag("11deadbeef2211deadbeef22")
    assert tag == None

    #insert tag 1:
    tag_id = await client.insert_tag(test_tag_1)
    tag = await client.request_tag(tag_id)
    assert compare_dict_without_id(tag, test_tag_1, ["id"])

    #insert tag 2:
    tag_id = await client.insert_tag(test_tag_2)
    tag = await client.request_tag(tag_id)
    assert compare_dict_without_id(tag, test_tag_2, ["id"])

    #request all tags:
    tags = await client.request_all_tags()
    assert compare_dict_without_id(tags[0], test_tag_1, ["id", "description"])
    assert compare_dict_without_id(tags[1], test_tag_2, ["id", "description"])

    #delete tag:
    tag_id = await client.insert_tag(test_tag_3)
    tag = await client.request_tag(tag_id)
    assert compare_dict_without_id(tag, test_tag_3, ["id"])
    result = await client.delete_tag(tag_id)
    assert result != None
    tag = await client.request_tag(tag_id)
    assert tag == None