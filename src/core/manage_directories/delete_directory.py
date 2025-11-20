import os
import shutil

# Diretoria base
base_dir = r"G:\History\Lyngsoe"

# Name of the directory to delete
target_dir_name = "20250818"
dir_path = os.path.join(base_dir, target_dir_name)

if dir_path and os.path.isdir(dir_path):
    print(f"[DELETE] {dir_path} and all files/subdirectories within")
    # Uncomment the line below to actually delete
    shutil.rmtree(dir_path)
else:
    print(f"[IGNORE] {dir_path} (does not exist or is not a valid directory)")
