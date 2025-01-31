import os
import shutil
import json
from datetime import datetime

def load_config():
    # Load configuration from config.json
    with open('config.json') as config_file:
        config = json.load(config_file)
    return config

def get_shaw_acct_number(folder_name):
    # Extracting the account number from the folder name
    parts = folder_name.strip().split('-')
    if len(parts) == 2:
        name, acct_number = parts
        acct_number = acct_number.strip()
        # Formatting the Shaw account number
        shaw_acct_number = f"50000{acct_number}0001"
        return shaw_acct_number
    else:
        return None

def copy_and_prefix_files(source_dir, destination_dir, log_file_path):
    # Print debug information to the console
    print(f"Source Directory: {source_dir}")
    print(f"Destination Directory: {destination_dir}")

    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return

    # Check if destination directory exists
    if not os.path.exists(destination_dir):
        print(f"Destination directory does not exist: {destination_dir}")
        return

    # Create a 'log' folder in the root directory if it doesn't exist
    script_directory = os.path.dirname(os.path.abspath(__file__))
    log_folder = os.path.join(script_directory, 'log')
    os.makedirs(log_folder, exist_ok=True)

    # Get the current date for logging
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Set the path for the log file in the 'log' folder with today's date
    log_file_path = os.path.join(log_folder, f"log_{current_date}.txt")

    # Open the log file in append mode
    with open(log_file_path, 'a') as log_file:
        # Write the current date to the log file
        log_file.write(f"\n\n---- {current_date} ----\n")

        # Iterate through the source directory
        for root, dirs, files in os.walk(source_dir):
            log_file.write(f"\nRoot: {root}\n")
            log_file.write(f"Directories: {dirs}\n")
            log_file.write(f"Files: {files}\n")
            
            for file_name in files:
                # Check if the file ends with "Pymnt History.pdf"
                if file_name.endswith("Pymnt History.pdf"):
                    source_path = os.path.join(root, file_name)
                    
                    # Get Shaw account number from the parent folder
                    folder_name = os.path.basename(root)
                    shaw_acct_number = get_shaw_acct_number(folder_name)
                    
                    if shaw_acct_number:
                        # Prefix the file with Shaw account number
                        new_file_name = f"{shaw_acct_number}_{file_name}"
                        
                        # Create the destination directory if it doesn't exist
                        destination_path = os.path.join(destination_dir, new_file_name)
                        
                        # Write copying information to the log file
                        log_file.write(f"Copying: {source_path} -> {destination_path}\n")
                        
                        # Copy the file to the destination
                        shutil.copyfile(source_path, destination_path)
                        
                        # Write file copied information to the log file
                        log_file.write(f"File copied: {source_path} -> {destination_path}\n")

if __name__ == "__main__":
    # Load configuration
    config = load_config()

    # Set your source and destination directories
    source_directory = config.get('source_directory', '')
    destination_directory = config.get('destination_directory', '')

    if source_directory and destination_directory:
        # Call the function to copy and prefix files
        copy_and_prefix_files(source_directory, destination_directory, '')
    else:
        print("Please provide valid source and destination directories in config.json.")
