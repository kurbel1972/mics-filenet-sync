import os
import shutil
from datetime import datetime, timedelta

# Directory base
base_dir = r"G:\History\Lyngsoe"
base_dir_lyngsoe = r"G:\Lyngsoe"

# Number of days to keep directories
days_threshold = 60

# Limit date calculation
limit_date = datetime.now() - timedelta(days=days_threshold)

print(f"Diretoria base: {base_dir}")
print(f"Data limite: {limit_date.strftime('%Y-%m-%d')}")

def remove_old_dirs_safe(path):
    print(f"Data limite: {limit_date.strftime('%Y-%m-%d')}")
    for dir_name in os.listdir(path):
        dir_path = os.path.join(path, dir_name)
        if not dir_path or not os.path.isdir(dir_path):
            print(f"[IGNORE] {dir_path} (not a valid directory)")
            continue
        try:
            dir_date = datetime.strptime(dir_name, "%Y%m%d")
            if dir_date < limit_date:
                # Confirm before deleting
                print(f"[DELETING] {dir_path}")                
                shutil.rmtree(dir_path)
            else:
                print(f"[KEEPING *****************************] {dir_path}")
        except ValueError:
            print(f"[IGNORE] {dir_path} (not a date in YYYYMMDD format)")

remove_old_dirs_safe(base_dir)
remove_old_dirs_safe(base_dir_lyngsoe)
