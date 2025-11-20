import os
import shutil
import logging

class FileHandler:
    def copy_file_to_destination(self, source_file, destination_folder):
        os.makedirs(destination_folder, exist_ok=True)
        file_name = os.path.basename(source_file)
        destination_path = os.path.join(destination_folder, file_name)
        if os.path.exists(destination_path):
            print(f"[SKIPPED] {file_name} already exists in {destination_folder}")
            logging.info(f"File {file_name} already exists in {destination_folder}, skipping copy.")
        else:
            shutil.copy(source_file, destination_path)
            print(f"[COPIED] {file_name} to {destination_path}")
            logging.info(f"File {file_name} copied to {destination_path}.")