from pymongo import MongoClient
from src.config.config import MONGODB_URI, MONGODB_DBNAME

if __name__ == "__main__":
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DBNAME]

    print("Creating index on 'objectNumber' in history_files...")
    db["history_files"].create_index("objectNumber")
    print("Index created in history_files.")

    print("Creating index on 'objectNumber' in filenet_status...")
    db["filenet_status"].create_index("objectNumber")
    print("Index created in filenet_status.")

    print("Done.")