from pymongo import MongoClient
from src.config.config import MONGODB_URI, MONGODB_DBNAME

def add_object_number(collection):
    docs = collection.find({})
    for doc in docs:
        file_name = doc.get("file_name")
        if file_name and len(file_name) >= 13:
            object_number = file_name[:13]
            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"objectNumber": object_number}}
            )
            print(f"Updated {file_name} with objectNumber {object_number}")

if __name__ == "__main__":
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DBNAME]

    print("Updating history_files...")
    add_object_number(db["history_files"])

    print("Updating filenet_status...")
    add_object_number(db["filenet_status"])

    print("Done.")