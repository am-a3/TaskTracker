from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class ProjectBasic(BaseModel):
    id: str
    name: str

class Project(ProjectBasic):
    description: Optional[str] = None

class Location(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class Tag(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class TaskBasic(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class Task(TaskBasic):
    project_id: Optional[str] = None
    location_id: Optional[str] = None
    is_done: str
    tags: Optional[list[str]] = None # tag ids