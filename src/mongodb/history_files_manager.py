from pymongo import MongoClient, errors
from datetime import datetime, timezone
from src.config.config import MONGODB_URI, MONGODB_DBNAME

class HistoryFilesManager:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DBNAME]
        self.collection = self.db["history_files"]
        # Garantir índice único em file_name
        self.collection.create_index("file_name", unique=True)

    def insert_file(self, file_doc, user="MICS-FILENET-SYNC"):
        if self.file_exists(file_doc["file_name"]):
            print(f"[SKIPPED] File '{file_doc['file_name']}' already exists in history_files.")
            return None
        now = datetime.now(timezone.utc)
        file_doc["created_at"] = now
        file_doc["updated_at"] = now
        file_doc["created_by"] = user
        file_doc["updated_by"] = user
        try:
            return self.collection.insert_one(file_doc)
        except errors.DuplicateKeyError:
            print(f"[SKIPPED] File '{file_doc['file_name']}' already exists (duplicate key).")
            return None

    def update_file(self, file_name, update_fields, user="MICS-FILENET-SYNC"):
        update_fields["updated_at"] = datetime.now(timezone.utc)
        update_fields["updated_by"] = user
        return self.collection.update_one(
            {"file_name": file_name},
            {"$set": update_fields}
        )

    def delete_file(self, file_name):
        return self.collection.delete_one({"file_name": file_name})

    def find_file(self, file_name):
        return self.collection.find_one({"file_name": file_name})

    def list_files(self, filter_dict=None):
        return list(self.collection.find(filter_dict or {}))

    def file_exists(self, file_name):
        return self.collection.count_documents({"file_name": file_name}) > 0

# Example usage:
if __name__ == "__main__":
    manager = HistoryFilesManager()