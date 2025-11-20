from pymongo import MongoClient
from src.config.config import MONGODB_URI, MONGODB_DBNAME

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DBNAME]

collections_to_create = ["history_files", "filenet_status"]
existing_collections = db.list_collection_names()

for collection in collections_to_create:
    if collection not in existing_collections:
        db.create_collection(collection)
        print(f"Collection '{collection}' created!")
    else:
        print(f"Collection '{collection}' already exists, skipped.")

# python -m src.mongodb.create_collections 