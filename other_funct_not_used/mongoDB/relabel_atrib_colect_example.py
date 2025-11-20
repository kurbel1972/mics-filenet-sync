from pymongo import MongoClient
from src.config.config import MONGODB_URI, MONGODB_DBNAME

def drop_index_if_exists(collection, index_name):
    indexes = collection.index_information()
    if index_name in indexes:
        collection.drop_index(index_name)
        print(f"Dropped index: {index_name}")

def remove_field(collection, field_name):
    result = collection.update_many(
        {field_name: {"$exists": True}},
        {"$unset": {field_name: ""}}
    )
    print(f"Removed field '{field_name}' from {result.modified_count} documents.")

def add_objectnumber(collection):
    docs = collection.find({})
    for doc in docs:
        file_name = doc.get("file_name")
        if file_name and len(file_name) >= 13:
            objectnumber = file_name[:13]
            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"objectnumber": objectnumber}}
            )
            print(f"Updated {file_name} with objectnumber {objectnumber}")

if __name__ == "__main__":
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DBNAME]

    for col_name in ["history_files", "filenet_status"]:
        print(f"\nProcessing {col_name}...")
        col = db[col_name]
        drop_index_if_exists(col, "objectNumber_1")
        remove_field(col, "objectNumber")
        add_objectnumber(col)
        col.create_index("objectnumber")
        print(f"Index created on 'objectnumber' in {col_name}")

    print("\nDone.")