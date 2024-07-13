from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from data_models import ProjectBasic, Project, LocationBasic, Location, Tag, TaskBasic, Task
from typing import List, Dict
from mongodb_client import MongoDbClient
from fastapi.encoders import jsonable_encoder

db_client = MongoDbClient("mongodb://localhost:27017/", "task_db")

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

@app.post("/projects/", response_model=Project)
async def create_project(project: Project):
    project_json = jsonable_encoder(project)
    await db_client.insert_project(project_json)
    return project

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

@app.post("/locations/", response_model=Location)
async def create_location(location: Location):
    location_json = jsonable_encoder(location)
    await db_client.insert_location(location_json)

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
    await db_client.insert_task(task_json)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    await db_client.delete_task(task_id)
    return {"message": "Task deleted successfully"}

# Tag related:

@app.get("/tags", response_model=List[Tag])
async def read_tags() -> list[Tag]:
    return [{"id": 0, "name": "tag"}]

@app.get("/tags/{tag_id}", response_model=Tag)
async def read_tag(tag_id: str) -> Tag:
    return {"id": tag_id, "name": "tag"}

@app.post("/tags/", response_model=Tag)
async def create_tag(tag: Tag):
    return tag
