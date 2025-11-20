from src.core.filenet.filenet_checker import FileNetChecker
from src.core.filenet.file_handler import FileHandler
from src.config.config import OUTPUT_FOLDER
from src.mongodb.filenet_status_manager import FileNetStatusManager
from datetime import datetime, timezone
import logging

class FileNetProcessor:
    def __init__(self, output_folder=OUTPUT_FOLDER):
        self.output_folder = output_folder
        self.checker = FileNetChecker()
        self.file_handler = FileHandler()
        self.status_manager = FileNetStatusManager()

    def process_files(self, files_for_filenet, date_input):
        for file_path, file_name in files_for_filenet:
            if self.status_manager.status_exists(file_name):
                print(f"  FileNet status already registered in MongoDB: {file_name}")
                logging.info(f"FileNet status already registered in MongoDB: {file_name}")
            else:
                print(f"  Checking in FileNet: {file_name}")
                logging.info(f"Checking in FileNet: {file_name}")
                exists = self.checker.file_exists_in_filenet(file_name)
                status_doc = {
                    "file_name": file_name,
                    "object_number": file_name[:13],
                    "checked_at": datetime.now(timezone.utc),
                    "mics_date": date_input,
                    "exists_in_filenet": exists,
                    "copied_to_recovery": False,
                    "error": None
                }
                if exists:
                    print(f"    [OK] {file_name} found in FileNet.")
                    logging.info(f"File {file_name} found in FileNet.")
                else:
                    print(f"    [MISSING] {file_name} not found in FileNet. Copying to destination.")
                    logging.info(f"File {file_name} not found in FileNet. Copying to destination.")
                    self.file_handler.copy_file_to_destination(file_path, self.output_folder)
                    status_doc["copied_to_recovery"] = True

                self.status_manager.insert_status(status_doc)