from fastapi import FastAPI
from contextlib import asynccontextmanager
from data_models import ProjectBasic, Project, Location, Tag, TaskBasic, Task
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

@app.get("/projects", response_model=List[ProjectBasic])
async def read_projects() -> list[ProjectBasic]:
    projects = await db_client.request_all_projects()
    return projects

@app.get("/projects/{project_id}", response_model=Project)
async def read_project(project_id: str) -> Project:
    return await db_client.request_project(project_id)

@app.get("/projects/{project_id}/tasks", response_model=List[TaskBasic])
async def read_project_tasks(project_id: str) -> list[dict]:
    tasks = await db_client.request_project_task(project_id)
    return tasks

@app.post("/projects/", response_model=Project)
async def create_project(project: Project):
    project_json = jsonable_encoder(project)
    await db_client.insert_project(project_json)
    return project

@app.get("/locations", response_model=List[Location])
async def read_locations() -> list[Location]:
    return [{"id": 0, "name": "location"}]

@app.get("/locations/{location_id}", response_model=Location)
async def read_location(location_id: str) -> Location:
    if location_id == "0":
        return {"id": location_id, "name": "location_0"}
    else:
        return {"id": location_id, "name": "location_1"}

@app.get("/locations/{location_id}/tasks", response_model=List[Task])
async def read_location_tasks(location_id: str) -> list[Task]:
    return [{"id": location_id, "name": "test"}]

@app.post("/locations/", response_model=Location)
async def create_location(location: Location):
    return location

@app.get("/tasks", response_model=List[Task])
async def read_tasks() -> list[dict]:
    return [{"id": 0, "name": "task"}]

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: str) -> Task:
    return {"id": task_id, "name": "task"}

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    return task

@app.get("/tags", response_model=List[Tag])
async def read_tags() -> list[Tag]:
    return [{"id": 0, "name": "tag"}]

@app.get("/tags/{tag_id}", response_model=Tag)
async def read_tag(tag_id: str) -> Tag:
    return {"id": tag_id, "name": "tag"}

@app.post("/tags/", response_model=Tag)
async def create_tag(tag: Tag):
    return tag
