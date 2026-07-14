import glob
import logging
import os
import subprocess
from datetime import datetime

from src.config.config import MONGODB_URI, MONGODB_DBNAME


class MongoDBBackupManager:
    def __init__(self, mongodump_exe_path: str, backup_dir: str):
        self.mongodump_exe_path = (mongodump_exe_path or "").strip()
        self.backup_dir = (backup_dir or "").strip()

    def _validate_paths(self) -> bool:
        if not self.mongodump_exe_path:
            logging.error("MongoDB backup aborted: mongodump.exe path was not provided.")
            print("MongoDB backup aborted: mongodump.exe path was not provided.")
            return False

        if not os.path.isfile(self.mongodump_exe_path):
            logging.error(f"MongoDB backup aborted: mongodump.exe was not found at '{self.mongodump_exe_path}'.")
            print(f"MongoDB backup aborted: mongodump.exe was not found at '{self.mongodump_exe_path}'.")
            return False

        if not self.backup_dir:
            logging.error("MongoDB backup aborted: backup destination directory was not provided.")
            print("MongoDB backup aborted: backup destination directory was not provided.")
            return False

        if not os.path.isdir(self.backup_dir):
            logging.error(f"MongoDB backup aborted: destination directory does not exist '{self.backup_dir}'.")
            print(f"MongoDB backup aborted: destination directory does not exist '{self.backup_dir}'.")
            return False

        return True

    def _build_archive_path(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_name = MONGODB_DBNAME or "mongodb_backup"
        filename = f"{db_name}_{timestamp}.gz"
        return os.path.join(self.backup_dir, filename)

    def _delete_old_backups(self, current_backup_path: str) -> None:
        db_name = MONGODB_DBNAME or "mongodb_backup"
        patterns = [
            os.path.join(self.backup_dir, f"{db_name}_*.gz"),
            os.path.join(self.backup_dir, "mics_filenet.gz"),
            os.path.join(self.backup_dir, f"{db_name}.gz"),
        ]

        backup_candidates = set()
        for pattern in patterns:
            backup_candidates.update(glob.glob(pattern))

        for backup_file in backup_candidates:
            if os.path.abspath(backup_file) == os.path.abspath(current_backup_path):
                continue
            try:
                os.remove(backup_file)
                logging.info(f"Deleted old MongoDB backup file: {backup_file}")
            except OSError as exc:
                logging.warning(f"Could not delete old MongoDB backup file '{backup_file}': {exc}")

    def run_backup(self) -> bool:
        if not self._validate_paths():
            return False

        archive_path = self._build_archive_path()
        command = [
            self.mongodump_exe_path,
            f"--uri={MONGODB_URI}",
            f"--db={MONGODB_DBNAME}",
            f"--archive={archive_path}",
            "--gzip",
        ]

        try:
            subprocess.run(command, check=True)
            logging.info(f"MongoDB backup created successfully: {archive_path}")
            print(f"MongoDB backup created successfully: {archive_path}")
            self._delete_old_backups(archive_path)
            return True
        except subprocess.CalledProcessError as exc:
            logging.exception(f"MongoDB backup failed with exit code {exc.returncode}: {exc}")
            print(f"MongoDB backup failed with exit code {exc.returncode}.")
            return False
        except Exception as exc:
            logging.exception(f"MongoDB backup failed due to an unexpected error: {exc}")
            print(f"MongoDB backup failed due to an unexpected error: {exc}")
            return False
