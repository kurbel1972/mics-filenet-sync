from pymongo import MongoClient, errors
from datetime import datetime, timezone
from src.config.config import MONGODB_URI, MONGODB_DBNAME

class FileNetStatusManager:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DBNAME]
        self.collection = self.db["filenet_status"]
        # Garantir índice único em file_name
        self.collection.create_index("file_name", unique=True)

    def insert_status(self, status_doc, user="MICS-FILENET-SYNC"):
        if self.status_exists(status_doc["file_name"]):
            print(f"[SKIPPED] Status for '{status_doc['file_name']}' already exists in filenet_status.")
            return None
        now = datetime.now(timezone.utc)
        status_doc["created_at"] = now
        status_doc["updated_at"] = now
        status_doc["created_by"] = user
        status_doc["updated_by"] = user
        try:
            return self.collection.insert_one(status_doc)
        except errors.DuplicateKeyError:
            print(f"[SKIPPED] Status for '{status_doc['file_name']}' already exists (duplicate key).")
            return None

    def update_status(self, file_name, update_fields, user="MICS-FILENET-SYNC"):
        update_fields["updated_at"] = datetime.now(timezone.utc)
        update_fields["updated_by"] = user
        return self.collection.update_one(
            {"file_name": file_name},
            {"$set": update_fields}
        )

    def delete_status(self, file_name):
        return self.collection.delete_one({"file_name": file_name})

    def find_status(self, file_name):
        return self.collection.find_one({"file_name": file_name})

    def list_status(self, filter_dict=None):
        return list(self.collection.find(filter_dict or {}))

    def status_exists(self, file_name):
        return self.collection.count_documents({"file_name": file_name}) > 0

# Example usage:
if __name__ == "__main__":
    manager = FileNetStatusManager()