#!/usr/bin/env python3

import os
import shutil
import datetime
import zipfile

def create_backup():
    # Get current directory
    current_dir = os.getcwd()
    project_name = "QuantumAvatar"

    # Timestamp für eindeutigen Namen
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"cash_money_backup_{timestamp}.zip"

    # Backup path
    backup_dir = os.path.join(current_dir, "backups")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backup_path = os.path.join(backup_dir, backup_name)

    # Create ZIP archive
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through all files in the current directory (excluding backups to avoid recursion)
        for root, dirs, files in os.walk(current_dir):
            # Exclude backups directory to avoid recursive backup
            if 'backups' in dirs:
                dirs.remove('backups')
            for file in files:
                file_path = os.path.join(root, file)
                # Add file to zip with relative path
                rel_path = os.path.relpath(file_path, current_dir)
                zipf.write(file_path, rel_path)

    print(f"Backup erstellt: {backup_path}")
    return backup_path

if __name__ == "__main__":
    create_backup()
