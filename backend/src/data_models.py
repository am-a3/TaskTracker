from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class ProjectBasic(BaseModel):
    id: str
    name: str

class Project(ProjectBasic):
    description: Optional[str] = None

class LocationBasic(BaseModel):
    id: str
    name: str

class Location(LocationBasic):
    description: Optional[str] = None

class TagBasic(BaseModel):
    id: str
    name: str

class Tag(TagBasic):
    description: Optional[str] = None

class TaskBasic(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class Task(TaskBasic):
    project_id: Optional[str] = None
    location_id: Optional[str] = None
    is_done: Optional[str] = None
    tags: Optional[list[str]] = None # tag ids