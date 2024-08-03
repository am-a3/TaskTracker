from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import api_v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Init database client")
    yield
    print("Deinit database client")

app = FastAPI(lifespan=lifespan)

app.include_router(api_v1.router, prefix="/v1")
