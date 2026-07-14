# mics-filenet-sync

Synchronizes files between MICS source folders and FileNet, and keeps an automated MongoDB backup at the end of each main execution.

## What The Project Does

The application runs a full operational flow:

1. Mount configured network drives.
2. Collect and copy history files for the selected date.
3. Validate files against FileNet and process missing items.
4. Run a MongoDB backup using mongodump and keep only the latest backup file.

## Main Features

- Date-based file collection from mapped drives.
- FileNet existence checks through configured endpoints.
- Processing pipeline for missing files.
- Automated MongoDB backup after processing.
- Backup cleanup policy that removes older backup files for the same database.

## MongoDB Backup Behavior

At step 4, the program asks for:

- Full path to mongodump.exe.
- Destination folder for backup files.

If you press Enter, values from .env are used as defaults.

Before running the backup, the script validates:

- The mongodump.exe file exists.
- The backup destination directory exists.

Generated backup format:

- mics_filenet_sync_YYYYMMDD_HHMMSS.gz

After a successful backup, older files matching the same database prefix are deleted, keeping only the latest backup.

## Environment Variables

Required values in .env include:

- USERNAME_FILENET
- PASSWORD_FILENET
- NETWORK_USERNAME
- NETWORK_PASSWORD
- DRIVE1, DRIVE2
- DRIVE1_PATH, DRIVE2_PATH
- DEST_DIR
- FILENET_URL_BASE
- FILENET_URL_OBJ_STORE
- MONGODB_URI
- MONGODB_DBNAME
- MONGODUMP_EXE_PATH
- MONGODB_BACKUP_DIR

Example for backup-related variables:

MONGODUMP_EXE_PATH=C:\Program Files\MongoDB\Server\8.0\bin\mongodump.exe
MONGODB_BACKUP_DIR=C:\MongoBackup

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies from requirements.txt.
4. Configure .env.
5. Run main.py.

## Notes

- Target environment is Windows.
- Ensure MongoDB tools are installed and mongodump.exe path is correct.
