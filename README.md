# mics-filenet-sync
<<<<<<< HEAD
Synchronize files on Filenet and Mics 
=======

A Python-based tool to collect `.tif` files from mapped drives based on a specific date, check if they exist in the FileNet CMIS repository, and copy only the missing files to a local directory.

This script is the main entry point for the file discovery and FileNet checking process.
It prompts the user for a date, scans the specified drives for .tif files with that date,
checks if those files exist in FileNet, and copies any missing files to a specified output folder.
The script uses functions from the file_discovery, filenet_checker, and file_handler modules
to perform its tasks. The main function orchestrates the flow of the program.
The script is designed to be run as a standalone program, and it will execute the main function
when run directly. The script is modular, with separate modules for file discovery,
FileNet checking, and file handling, making it easy to maintain and extend.
The script is designed to be run in a Windows environment, as indicated by the use of
Windows-style paths in the file handling functions. The script is also designed to be
user-friendly, with clear output messages indicating the status of each file being processed.

## Features

- **Date-based search:** Scans for `.tif` files on multiple mapped drives filtered by a date provided by the user.
- **FileNet check:** Queries the FileNet repository via CMIS to verify if each file exists.
- **Automatic file transfer:** Copies missing files to a designated local folder.
- **Modular design:** Follows best practices with separate modules and environment variable configurations.

## Project Structure

mics-filenet-sync/
├── main.py # Entry point of the application
├── config.py # Loads environment variables from .env
├── file_discovery.py # Scans mapped drives for .tif files by date
├── filenet_checker.py # Checks file existence in the FileNet repository
├── file_handler.py # Copies missing files to the destination folder
├── .env # Environment variables (should not be committed)
├── requirements.txt # List of required Python packages
└── README.md # Project documentation


## Setup

1. **Clone the repository:**

   ```bash
   git clone <repo-url>
   cd mics-filenet-sync

2. **Create and activate a virtual environment:**
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Linux/macOS:
source venv/bin/activate

3. **Install dependencies:**

pip install -r requirements.txt
>>>>>>> 9aec157 (First commit)
