import os
from datetime import datetime
import logging

def list_tif_files_by_date(drive, date_str):
    """
    Search for .tif files in the given drive that have a date matching date_str.
    Expected file naming format: <prefix>_<id>_YYYYMMDDhhmmssXX<rest>.tif
    """
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    valid_files = []

    # Ensure drive path ends with a separator
    logging.info(f"Listing .tif files in drive: {drive} for date: {date_str}")
    drive_path = drive if drive.endswith(os.sep) else drive + os.sep

    # List only .tif files
    tif_files = [f for f in os.listdir(drive_path) if f.lower().endswith(".tif")]

    for file_name in tif_files:
        parts = file_name.split("_")
        if len(parts) >= 3:
            # Extract the date part (first 8 characters of the third segment)
            date_part = parts[2][:8]
            try:
                file_date = datetime.strptime(date_part, "%Y%m%d")
                if file_date.date() == target_date.date():
                    print(f" File matches date: {file_name}")
                    logging.info(f"File matches date: {file_name}")
                    # Append tuple (full path, datetime string for sorting)
                    valid_files.append((os.path.join(drive_path, file_name), parts[2]))
            except ValueError:
                continue

    # Sort by the full datetime string in descending order
    valid_files.sort(key=lambda x: x[1], reverse=True)
    # Return only the file paths
    return [file_path for file_path, _ in valid_files]