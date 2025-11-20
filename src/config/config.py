from dotenv import load_dotenv
import os

load_dotenv()

USERNAME_FILENET = os.getenv("USERNAME_FILENET")
PASSWORD_FILENET = os.getenv("PASSWORD_FILENET")
DRIVES = [os.getenv("DRIVE1"), os.getenv("DRIVE2")]
DRIVE_PATHS = [os.getenv("DRIVE1_PATH"), os.getenv("DRIVE2_PATH")]
# DRIVES = [os.getenv("DRIVE1")]
# DRIVE_PATHS = [os.getenv("DRIVE1_PATH")]
NETWORK_USERNAME = os.getenv("NETWORK_USERNAME")
NETWORK_PASSWORD = os.getenv("NETWORK_PASSWORD")
OUTPUT_FOLDER = os.getenv("DEST_DIR")
FILENET_BASE_URL = os.getenv("FILENET_URL_BASE")
FILENET_URL_OBJ_STORE = os.getenv("FILENET_URL_OBJ_STORE")
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")