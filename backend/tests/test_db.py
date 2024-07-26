import pytest
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath('../src'))

from mongodb_client import MongoDbClient
from common_utils import compare_dict_without_id, clear_db, test_project_1, test_project_2, test_project_3

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