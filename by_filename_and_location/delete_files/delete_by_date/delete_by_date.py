import os
import json
import logging
from datetime import datetime

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def is_modified_on_date(path, target_date):
    try:
        # Get the last modified time of the file/directory
        modified_time = os.path.getmtime(path)
        modified_date = datetime.fromtimestamp(modified_time).date()
        return modified_date == target_date
    except OSError as e:
        print(f"Error accessing {path}: {e}")
        return False

def delete_files_and_directories(target_directory, target_date):
    print(f"Deleting files and directories modified on {target_date}...")
    for root, dirs, files in os.walk(target_directory, topdown=False):
        # Check and delete files
        for name in files:
            file_path = os.path.join(root, name)
            if is_modified_on_date(file_path, target_date):
                print(f"Deleting file: {file_path}")
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    else:
                        print(f"File does not exist: {file_path}")
                except OSError as e:
                    print(f"Failed to delete file: {file_path}. Reason: {e}")
        
        # Check and delete directories (including contents)
        for name in dirs:
            dir_path = os.path.join(root, name)
            if is_modified_on_date(dir_path, target_date):
                print(f"Deleting directory: {dir_path}")
                delete_directory_contents(dir_path)
                try:
                    if os.path.exists(dir_path):
                        os.rmdir(dir_path)
                        print(f"Deleted directory: {dir_path}")
                    else:
                        print(f"Directory does not exist: {dir_path}")
                except OSError as e:
                    print(f"Failed to delete directory: {dir_path}. Reason: {e}")

def delete_directory_contents(directory):
    # Recursively delete all contents of a directory
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                else:
                    print(f"File does not exist: {file_path}")
            except OSError as e:
                print(f"Failed to delete file: {file_path}. Reason: {e}")
        
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                if os.path.exists(dir_path):
                    os.rmdir(dir_path)
                    print(f"Deleted directory: {dir_path}")
                else:
                    print(f"Directory does not exist: {dir_path}")
            except OSError as e:
                print(f"Failed to delete directory: {dir_path}. Reason: {e}")

def main():
    # Configure logging
    log_filename = datetime.now().strftime('delete_log_%Y-%m-%d_%H-%M-%S.log')
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

    config = load_config('config.json')
    target_directory = config['target_directory']
    target_date = datetime.strptime(config['target_date'], '%Y-%m-%d').date()

    print(f"Deleting files and directories modified on {target_date}...")
    delete_files_and_directories(target_directory, target_date)

if __name__ == "__main__":
    main()
