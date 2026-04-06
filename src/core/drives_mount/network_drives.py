import os
import subprocess
from src.config.config import DRIVES, DRIVE_PATHS, NETWORK_USERNAME, NETWORK_PASSWORD
import time
import logging

class NetworkDriveManager:
    def __init__(self, drives=DRIVES, paths=DRIVE_PATHS, username=NETWORK_USERNAME, password=NETWORK_PASSWORD):
        self.drives = drives
        self.paths = paths
        self.username = username
        self.password = password

    def unmap_drive(self, drive):
        logging.info(f"Unmapping {drive} if mapped...")
        try:
            command = f'net use {drive} /delete /y'
            print(f"Unmapping {drive} if mapped...")
            subprocess.run(command, capture_output=True, text=True, shell=True)
            time.sleep(1)  # Pequeno delay para garantir que o Windows processa o unmap
            logging.info(f"Unmapped {drive} successfully.")
        except Exception as e:
            print(f"Exception while unmapping {drive}: {str(e)}")

    def map_drive(self, drive, path):
        print(f" Mapping {drive} to {path} ...")
        logging.info(f"Mapping {drive} to {path} ...")
        try:
            self.unmap_drive(drive)  # Unmap sempre antes de mapear
            if self.username and self.password:
                command = f'net use {drive} "{path}" {self.password} /user:{self.username} /persistent:yes'
            else:
                command = f'net use {drive} "{path}" /persistent:yes'
            print(f"Executing command: {command}")
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                print(f" Failed to map {drive}: {result.stderr.strip()}")
                logging.warning(f"Failed to map {drive} to {path}: {result.stderr.strip()}")
                return False
            else:
                print(f" Drive {drive} mapped successfully.")
                logging.info(f"Mapped {drive} to {path} successfully.")
                return True
        except Exception as e:
            print(f" Exception while mapping {drive}: {str(e)}")
            logging.error(f"Error mapping {drive} to {path}: {str(e)}")
            return False

    def mount_network_drives(self):
        logging.info("Mounting network drives...")
        mounted_drives = []
        for drive, path in zip(self.drives, self.paths):
            if not (drive and path):
                continue
            if self.map_drive(drive, path):  # Tenta sempre montar
                mounted_drives.append(drive)
        logging.info(f"Finished mounting network drives. Successfully mounted: {mounted_drives}")
        return mounted_drives

if __name__ == "__main__":
    manager = NetworkDriveManager()
    manager.mount_network_drives()