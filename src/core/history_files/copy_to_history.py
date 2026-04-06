import os
from shutil import copy2
from src.core.history_files.file_discovery import list_tif_files_by_date
from src.config.config import DRIVES
from src.mongodb.history_files_manager import HistoryFilesManager
import logging


class HistoryCopier:
    def __init__(self, date_input, mounted_drives=None):
        self.date_input = date_input
        self.base_dir = os.path.join("G:\\Lyngsoe", date_input.replace("-", ""))
        self.history_dir = os.path.join("G:\\History\\Lyngsoe", date_input.replace("-", ""))
        self.db_manager = HistoryFilesManager()
        # Use mounted_drives if provided, otherwise fallback to DRIVES from config
        self.drives = mounted_drives if mounted_drives is not None else DRIVES

    def ensure_dir(self, path):
        logging.info(f"Ensuring directory exists: {path}")
        if not os.path.exists(path):
            os.makedirs(path)
            print(f" Directory created: {path}")
            logging.info(f"Directory created: {path}")
        else:
            print(f" Directory already exists: {path}")
            logging.info(f"Directory already exists: {path}")

    def handle_file(self, file_path, all_files):
        logging.info(f"Handling file: {file_path}")
        file_name = os.path.basename(file_path)
        all_files.append((file_path, file_name))
        if self.db_manager.file_exists(file_name):
            print(f"  History Files Already registered in MongoDB: {file_name}")
            logging.info(f"File already registered in MongoDB: {file_name}")
            return
        dest_path = os.path.join(self.history_dir, file_name)
        if os.path.exists(dest_path):
            print(f"  File already exists in history directory: {dest_path}")
            logging.info(f"File already exists in history directory: {dest_path}")
        else:
            copy2(file_path, dest_path)
            print(f" Copied to history: {dest_path}")
        file_doc = {
            "file_name": file_name,
            "object_number": file_name[:13],
            "history_path": dest_path,
            "mics_date": self.date_input,
            "copied_to_history": True
        }
        self.db_manager.insert_file(file_doc)
        logging.info(f"File {file_name} copied to history and registered in MongoDB.")

    def copy_files_to_history(self):
        logging.info(f"Starting copy of files to history for date: {self.date_input}")
        self.ensure_dir(self.base_dir)
        self.ensure_dir(self.history_dir)

        all_files = []
        for drive in map(str.strip, self.drives):
            print(f"\n Scanning drive: {drive}")
            logging.info(f"Scanning drive: {drive}")
            tif_files = list_tif_files_by_date(drive, self.date_input)
            if not tif_files:
                print("  No .tif files found on this drive.")
                logging.info(f"No .tif files found on drive: {drive}")
                continue
            for file_path in tif_files:
                self.handle_file(file_path, all_files)


        print(f"\n Total files copied and registered: {len(all_files)}")
        logging.info(f"Total files copied and registered: {len(all_files)}")
        logging.info("Finished copying files to history.")
        return all_files