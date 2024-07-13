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

    def __to_dict(self, item: dict) -> dict:
        item = item.copy()  # Make a copy to avoid modifying the original document
        if "_id" in item and isinstance(item["_id"], ObjectId):
            item["id"] = str(item["_id"])
        return item

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
    
    async def request_project_task(self, project_id: str) -> list[dict]:
        task_collection = self.db[TASK_COLLECTION_NAME]
        cursor = task_collection.find({ "project_id": ObjectId(project_id) })
        tasks = await cursor.to_list(None)
        return [self.__to_dict(task) for task in tasks]

    async def insert_project(self, project: dict) -> ObjectId:
        project_collection = self.db[PROJECT_COLLECTION_NAME]
        del project["id"]
        result = await project_collection.insert_one(project)
        return result
    
if __name__ == '__main__':
    db_client = MongoDbClient("mongodb://localhost:27017/", "task_db")
    loop = asyncio.new_event_loop()
    data = loop.run_until_complete(db_client.request_project("668c52c347f7771ecb56d4b0"))
    