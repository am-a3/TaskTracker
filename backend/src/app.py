from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from data_models import ProjectBasic, Project, LocationBasic, Location, TagBasic, Tag, TaskBasic, Task
from typing import List
from mongodb_client import MongoDbClient
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
import os

load_dotenv()
if os.getenv('USE_TEST_DB', 'False') == 'True':
    db_client = MongoDbClient(os.getenv('DB_URL'), os.getenv('TEST_DB_NAME'))
else:
    db_client = MongoDbClient(os.getenv('DB_URL'), os.getenv('DB_NAME'))

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Init database client")
    yield
    print("Deinit database client")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Project related:

@app.get("/projects", response_model=List[ProjectBasic])
async def read_projects() -> list[ProjectBasic]:
    projects = await db_client.request_all_projects()
    return projects

@app.get("/projects/{project_id}", response_model=Project)
async def read_project(project_id: str) -> Project | None:
    project = await db_client.request_project(project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@app.get("/projects/{project_id}/tasks", response_model=List[TaskBasic])
async def read_project_tasks(project_id: str) -> list[dict]:
    tasks = await db_client.request_project_task(project_id)
    return tasks

@app.post("/projects/")
async def create_project(project: Project):
    project_json = jsonable_encoder(project)
    __id = await db_client.insert_project(project_json)
    return {"id":__id}

@app.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    await db_client.delete_project(project_id)
    return {"message": "Project deleted successfully"}

# Location related:

@app.get("/locations", response_model=List[LocationBasic])
async def read_locations() -> list[LocationBasic]:
    locations = await db_client.request_all_locations()
    return locations

@app.get("/locations/{location_id}", response_model=Location)
async def read_location(location_id: str) -> Location:
    location = await db_client.request_location(location_id)

    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    return location

@app.get("/locations/{location_id}/tasks", response_model=List[TaskBasic])
async def read_location_tasks(location_id: str) -> list[TaskBasic]:
    tasks = await db_client.request_location_task(location_id)
    return tasks

@app.post("/locations/")
async def create_location(location: Location):
    location_json = jsonable_encoder(location)
    __id = await db_client.insert_location(location_json)
    return {"id":__id}

@app.delete("/locations/{location_id}")
async def delete_location(location_id: str):
    await db_client.delete_location(location_id)
    return {"message": "Location deleted successfully"}

# Task related:

@app.get("/tasks", response_model=List[TaskBasic])
async def read_tasks() -> list[dict]:
    tasks = await db_client.request_all_tasks()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: str) -> Task:
    task = await db_client.request_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task_json = jsonable_encoder(task)
    __id = await db_client.insert_task(task_json)
    return {"id":__id}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    await db_client.delete_task(task_id)
    return {"message": "Task deleted successfully"}

# Tag related:

@app.get("/tags", response_model=List[TagBasic])
async def read_tags() -> list[Tag]:
    tags = await db_client.request_all_tags()
    return tags

@app.get("/tags/{tag_id}", response_model=Tag)
async def read_tag(tag_id: str) -> Tag:
    tag = await db_client.request_tag(tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag

@app.post("/tags/", response_model=Tag)
async def create_tag(tag: Tag):
    tag_json = jsonable_encoder(tag)
    __id = await db_client.insert_tag(tag_json)
    return {"id":__id}

@app.delete("/tags/{tag_id}")
async def delete_tag(tag_id: str):
    await db_client.delete_tag(tag_id)
    return {"message": "Tag deleted successfully"}
