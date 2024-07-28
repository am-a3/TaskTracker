import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
sys.path.append(os.path.abspath('../src'))

test_project_1 = {"id" : "0", "name": "project test", "description" : "For testing"}
test_project_2 = {"id" : "0", "name": "project test 2", "description" : "For testing 2"}
test_project_3 = {"id" : "0", "name": "project test 3", "description" : "For testing 3"}

test_location_1 = {"id" : "0", "name": "location test", "description" : "For testing"}
test_location_2 = {"id" : "0", "name": "location test 2", "description" : "For testing 2"}
test_location_3 = {"id" : "0", "name": "location test 3", "description" : "For testing 3"}

test_task_1 = {"id" : "0", "name": "task test", "description" : "For testing"}
test_task_2 = {"id" : "0", "name": "task test 2", "description" : "For testing 2"}
test_task_3 = {"id" : "0", "name": "task test 3", "description" : "For testing 3"}

test_tag_1 = {"id" : "0", "name": "tag test", "description" : "For testing"}
test_tag_2 = {"id" : "0", "name": "tag test 2", "description" : "For testing 2"}
test_tag_3 = {"id" : "0", "name": "tag test 3", "description" : "For testing 3"}

NOT_VALID_ID = "1234a"

def compare_dict_without_id(test: dict, reference: dict, exclude: list[str]) -> bool:
    for key in reference:
        if key in exclude:
            continue

        if key in test:
            if test[key] != reference[key]:
                print(f"[ERROR] Key {key} reference value is {reference[key]} and test value {test[key]}")
                return False
        else:
            print(f"[ERROR] Key {key} not present in test dictionary")
            return False
        
    return True

async def clear_db():
    load_dotenv()
    client = AsyncIOMotorClient(os.getenv('DB_URL'))
    db = client[os.getenv('TEST_DB_NAME')]
    collections = await db.list_collection_names()

    # Drop each collection
    for collection_name in collections:
        await db.drop_collection(collection_name)
        print(f"Dropped collection: {collection_name}")

    # Optionally, close the client connection
    client.close()
    return True