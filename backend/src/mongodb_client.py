from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio

PROJECT_COLLECTION_NAME = "projects"
LOCATION_COLLECTION_NAME = "locations"
TAG_COLLECTION_NAME = "tags"
TASK_COLLECTION_NAME = "tasks"

class MongoDbClient:
    def __init__(self, url: str, db_name: str):
        self.client = AsyncIOMotorClient(url)
        self.db = self.client[db_name]

    def __del__(self):
        self.client.close()

    def __to_dict(self, item: dict) -> dict:
        item = item.copy()  # Make a copy to avoid modifying the original document
        if "_id" in item and isinstance(item["_id"], ObjectId):
            item["id"] = str(item["_id"])
        return item

# Project related:

    async def request_all_projects(self) -> list[dict]:
        project_collection = self.db[PROJECT_COLLECTION_NAME]
        cursor = project_collection.find({},{ "description": 0 })
        projects = await cursor.to_list(None)
        return [self.__to_dict(prj) for prj in projects]

    async def request_project(self, project_id: str) -> dict | None:
        project_collection = self.db[PROJECT_COLLECTION_NAME]
        project = await project_collection.find_one({"_id": ObjectId(project_id)})
        if project is not None:
            project["id"] = str(project["_id"])
        return project

    async def request_project_tasks(self, project_id: str) -> list[dict]:
        task_collection = self.db[TASK_COLLECTION_NAME]
        cursor = task_collection.find({ "project_id": ObjectId(project_id) })
        tasks = await cursor.to_list(None)
        return [self.__to_dict(task) for task in tasks]

    async def insert_project(self, project: dict) -> ObjectId:
        project_collection = self.db[PROJECT_COLLECTION_NAME]
        del project["id"]
        result = await project_collection.insert_one(project)
        return str(result.inserted_id)
    
    async def delete_project(self, project_id: str) -> ObjectId | None:
        project_collection = self.db[PROJECT_COLLECTION_NAME]
        result = await project_collection.delete_one({"_id": ObjectId(project_id)})
        if result.deleted_count != 1:
            return None
        return ObjectId(project_id)

# Location related:

    async def request_all_locations(self) -> list[dict]:
        location_collection = self.db[LOCATION_COLLECTION_NAME]
        cursor = location_collection.find({},{ "description": 0 })
        locations = await cursor.to_list(None)
        return [self.__to_dict(loc) for loc in locations]

    async def request_location(self, location_id: str) -> dict | None:
        location_collection = self.db[LOCATION_COLLECTION_NAME]
        location = await location_collection.find_one({"_id": ObjectId(location_id)})
        if location is not None:
            location["id"] = str(location["_id"])
        return location

    async def request_location_task(self, location_id: str) -> list[dict]:
        task_collection = self.db[TASK_COLLECTION_NAME]
        cursor = task_collection.find({ "location_id": ObjectId(location_id) })
        tasks = await cursor.to_list(None)
        return [self.__to_dict(task) for task in tasks]
    
    async def insert_location(self, location: dict) -> ObjectId:
        location_collection = self.db[LOCATION_COLLECTION_NAME]
        del location["id"]
        result = await location_collection.insert_one(location)
        return str(result.inserted_id)
    
    async def delete_location(self, location_id: str) -> ObjectId | None:
        location_collection = self.db[LOCATION_COLLECTION_NAME]
        result = await location_collection.delete_one({"_id": ObjectId(location_id)})
        if result.deleted_count != 1:
            return None
        return ObjectId(location_id)

# Task related:
    async def request_all_tasks(self) -> list[dict]:
        task_collection = self.db[TASK_COLLECTION_NAME]
        cursor = task_collection.find({},{ "description": 0 })
        tasks = await cursor.to_list(None)
        return [self.__to_dict(task) for task in tasks]
    
    async def request_task(self, task_id: str) -> dict:
        task_collection = self.db[TASK_COLLECTION_NAME]
        task = await task_collection.find_one({"_id": ObjectId(task_id)})
        if task is not None:
            task["id"] = str(task["_id"])
        return task
    
    async def insert_task(self, task: dict) -> ObjectId:
        task_collection = self.db[TASK_COLLECTION_NAME]
        del task["id"]
        result = await task_collection.insert_one(task)
        return str(result.inserted_id)
    
    async def delete_task(self, task_id: str) -> ObjectId | None:
        task_collection = self.db[TASK_COLLECTION_NAME]
        result = await task_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count != 1:
            return None
        return ObjectId(task_id)

# Tags related:

    async def request_all_tags(self) -> list[dict]:
        tag_collection = self.db[TAG_COLLECTION_NAME]
        cursor = tag_collection.find({},{ "description": 0 })
        tags = await cursor.to_list(None)
        return [self.__to_dict(tag) for tag in tags]
    
    async def request_tag(self, tag_id: str) -> dict:
        tag_collection = self.db[TAG_COLLECTION_NAME]
        tag = await tag_collection.find_one({"_id": ObjectId(tag_id)})
        if tag is not None:
            tag["id"] = str(tag["_id"])
        return tag
    
    async def insert_tag(self, tag: dict) -> ObjectId:
        tag_collection = self.db[TAG_COLLECTION_NAME]
        del tag["id"]
        result = await tag_collection.insert_one(tag)
        return str(result.inserted_id)
    
    async def delete_tag(self, tag_id: str) -> ObjectId | None:
        tag_collection = self.db[TAG_COLLECTION_NAME]
        result = await tag_collection.delete_one({"_id": ObjectId(tag_id)})
        if result.deleted_count != 1:
            return None
        return ObjectId(tag_id)

if __name__ == '__main__':
    db_client = MongoDbClient("mongodb://localhost:27017/", "task_db")
    loop = asyncio.new_event_loop()
    data = loop.run_until_complete(db_client.request_project("668c52c347f7771ecb56d4b0"))
    