import os
from fastapi import HTTPException, APIRouter
from data_models import ProjectBasic, Project, LocationBasic, Location, TagBasic, Tag, TaskBasic, Task
from typing import List
from mongodb_client import MongoDbClient
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from bson import ObjectId

router = APIRouter()

def __is_id_valid(id: str):
    if ObjectId.is_valid(id):
        return True
    else:
        return False

load_dotenv()
if os.getenv('USE_TEST_DB', 'False') == 'True':
    db_client = MongoDbClient(os.getenv('DB_URL'), os.getenv('TEST_DB_NAME'))
else:
    db_client = MongoDbClient(os.getenv('DB_URL'), os.getenv('DB_NAME'))

@router.get("/")
async def root():
    return {"message": "Hello World"}

# Project related:

@router.get("/projects", response_model=List[ProjectBasic])
async def read_projects() -> list[ProjectBasic]:
    projects = await db_client.request_all_projects()
    return projects

@router.get("/projects/{project_id}", response_model=Project)
async def read_project(project_id: str) -> Project | None:
    if __is_id_valid(project_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    project = await db_client.request_project(project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@router.get("/projects/{project_id}/tasks", response_model=List[TaskBasic])
async def read_project_tasks(project_id: str) -> list[dict]:
    if __is_id_valid(project_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    tasks = await db_client.request_project_task(project_id)
    return tasks

@router.post("/projects/")
async def create_project(project: Project):
    project_json = jsonable_encoder(project)
    __id = await db_client.insert_project(project_json)
    return {"id":__id}

@router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, project: Project):
    project_json = jsonable_encoder(project)
    result = await db_client.update_project(project_json, project_id)
    if result == False:
        raise HTTPException(status_code=400, detail="Failed to update")
    
    return project_json

@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    if __is_id_valid(project_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    await db_client.delete_project(project_id)
    return {"message": "Project deleted successfully"}

# Location related:

@router.get("/locations", response_model=List[LocationBasic])
async def read_locations() -> list[LocationBasic]:
    locations = await db_client.request_all_locations()
    return locations

@router.get("/locations/{location_id}", response_model=Location)
async def read_location(location_id: str) -> Location:
    if __is_id_valid(location_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    location = await db_client.request_location(location_id)

    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    return location

@router.get("/locations/{location_id}/tasks", response_model=List[TaskBasic])
async def read_location_tasks(location_id: str) -> list[TaskBasic]:
    if __is_id_valid(location_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    tasks = await db_client.request_location_task(location_id)
    return tasks

@router.post("/locations/")
async def create_location(location: Location):
    location_json = jsonable_encoder(location)
    __id = await db_client.insert_location(location_json)
    return {"id":__id}

@router.put("/locations/{location_id}", response_model=Location)
async def update_location(location_id: str, location: Location):
    location_json = jsonable_encoder(location)
    result = await db_client.update_location(location_json, location_id)
    if result == False:
        raise HTTPException(status_code=400, detail="Failed to update")
    
    return location_json

@router.delete("/locations/{location_id}")
async def delete_location(location_id: str):
    if __is_id_valid(location_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    await db_client.delete_location(location_id)
    return {"message": "Location deleted successfully"}

# Task related:

@router.get("/tasks", response_model=List[TaskBasic])
async def read_tasks() -> list[dict]:
    tasks = await db_client.request_all_tasks()
    return tasks

@router.get("/tasks/done", response_model=List[TaskBasic])
async def read_tasks() -> list[dict]:
    tasks = await db_client.request_tasks_done(True)
    return tasks

@router.get("/tasks/not_done", response_model=List[TaskBasic])
async def read_tasks() -> list[dict]:
    tasks = await db_client.request_tasks_done(False)
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: str) -> Task:
    if __is_id_valid(task_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    task = await db_client.request_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.post("/tasks/")
async def create_task(task: Task):
    task_json = jsonable_encoder(task)
    __id = await db_client.insert_task(task_json)
    return {"id":__id}

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: Task):
    task_json = jsonable_encoder(task)
    result = await db_client.update_task(task_json, task_id)
    if result == False:
        raise HTTPException(status_code=400, detail="Failed to update")
    
    return task_json

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    if __is_id_valid(task_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    await db_client.delete_task(task_id)
    return {"message": "Task deleted successfully"}

# Tag related:

@router.get("/tags", response_model=List[TagBasic])
async def read_tags() -> list[Tag]:
    tags = await db_client.request_all_tags()
    return tags

@router.get("/tags/{tag_id}", response_model=Tag)
async def read_tag(tag_id: str) -> Tag:
    if __is_id_valid(tag_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    tag = await db_client.request_tag(tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag

@router.post("/tags/")
async def create_tag(tag: Tag):
    tag_json = jsonable_encoder(tag)
    __id = await db_client.insert_tag(tag_json)
    return {"id":__id}

@router.put("/tags/{tag_id}", response_model=Tag)
async def update_tag(tag_id: str, tag: Tag):
    tag_json = jsonable_encoder(tag)
    result = await db_client.update_tag(tag_json, tag_id)
    if result == False:
        raise HTTPException(status_code=400, detail="Failed to update")
    
    return tag_json

@router.delete("/tags/{tag_id}")
async def delete_tag(tag_id: str):
    if __is_id_valid(tag_id) == False:
        raise HTTPException(status_code=400, detail="ID is not valid")

    await db_client.delete_tag(tag_id)
    return {"message": "Tag deleted successfully"}