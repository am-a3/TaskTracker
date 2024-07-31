import os
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from .data_models import ProjectBasic, Project, LocationBasic, Location, TagBasic, Tag, TaskBasic, Task
from typing import List
from .mongodb_client import MongoDbClient
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from bson import ObjectId
from .routers import api_v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Init database client")
    yield
    print("Deinit database client")

app = FastAPI(lifespan=lifespan)

app.include_router(api_v1.router, prefix="/v1")
