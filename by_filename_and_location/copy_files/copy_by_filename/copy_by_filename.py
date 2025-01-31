import os
import shutil
import json
import logging
import datetime
import sys

class Config:
    def __init__(self, source_directory, destination_directory, file_string, max_files, max_files_value):
        self.source_directory = source_directory
        self.destination_directory = destination_directory
        self.file_string = file_string
        self.max_files = max_files
        self.max_files_value = max_files_value

def setup_logger(log_file_name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

def copy_files(config, logger):
    source_directory = config.source_directory
    destination_directory = config.destination_directory
    file_strings = config.file_string
    max_files = config.max_files
    max_files_value = config.max_files_value

    files_copied = 0
    matched_and_copied = 0  # Initialize the counter
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    file_copy_log_name = f"{current_date}_file_copy_log.txt"
    copied_files = set()  # Set to store copied files

    # Dictionary to count the number of files copied for each file string
    file_string_counts = {s: 0 for s in file_strings}

    with open(file_copy_log_name, 'a+') as file_copy_log:
        for root, dirs, files in os.walk(source_directory):
            for directory in dirs:
                directory_path = os.path.join(root, directory)
                file_count = len(os.listdir(os.path.join(root, directory)))
                print(f"Traversing directory: {directory_path} - Found {file_count} file(s)")
                # Write to log file
                file_copy_log.write(f"Traversing directory: {directory_path} - Found {file_count} file(s)\n")

                # Counting and copying matched files in this subdirectory
                matched_files_in_dir = 0
                for filename in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, filename)
                    for s in file_strings:
                        if s in filename:
                            matched_files_in_dir += 1
                            # Get the root directory name
                            destination_path = os.path.join(destination_directory, os.path.basename(os.path.dirname(file_path)))
                            os.makedirs(destination_path, exist_ok=True)  # Ensure destination directory exists
                            if file_path not in copied_files:  # Check if file is already copied
                                # Copy the file to the destination directory
                                shutil.copy(file_path, destination_path)
                                files_copied += 1
                                copied_files.add(file_path)  # Add copied file to the set
                                file_string_counts[s] += 1  # Increment count for this file string
                                # Print information only when files are matched and copied
                                if files_copied == 1:
                                    print(f"Source Directory: {source_directory}")
                                    print(f"Traversing directory: {root}")
                                    file_copy_log.write(f"Source Directory: {source_directory}\n")
                                    file_copy_log.write(f"Traversing directory: {root}\n")
                                print(f"Copying {file_path} to {destination_path}")
                                file_copy_log.write(f"Copying {file_path} to {destination_path}\n")
                                print("Matched: Yes")
                                file_copy_log.write("Matched: Yes\n")
                                # Check if the maximum number of files has been reached
                                if max_files and files_copied >= max_files_value:
                                    print(f"Max files limit reached. {max_files_value} files copied.")
                                    file_copy_log.write(f"Max files limit reached. {max_files_value} files copied.\n")
                                    # Log the counts for each file string before exiting
                                    file_copy_log.write("\nFiles copied for each file string:\n")
                                    for key, value in file_string_counts.items():
                                        file_copy_log.write(f"{key}: {value}\n")
                                    sys.exit()  # Exit the application after reaching the maximum files value
                # Check if the maximum number of files has been reached
                if max_files and files_copied >= max_files_value:
                    # Log the counts for each file string before exiting
                    file_copy_log.write("\nFiles copied for each file string:\n")
                    for key, value in file_string_counts.items():
                        file_copy_log.write(f"{key}: {value}\n")
                    sys.exit()  # Exit the application after reaching the maximum files value

                print(f"Matched files in {directory_path}: {matched_files_in_dir}")
                file_copy_log.write(f"Matched files in {directory_path}: {matched_files_in_dir}\n")
                matched_and_copied += matched_files_in_dir

        print("All files checked.")
        file_copy_log.write("All files checked.\n")

        # Log the counts for each file string at the end
        file_copy_log.write("\nFiles copied for each file string:\n")
        for key, value in file_string_counts.items():
            file_copy_log.write(f"{key}: {value}\n")

        # Check if the destination directory is empty
        if not os.listdir(destination_directory):
            print(f"Destination directory {destination_directory} is empty. Copying root directory.")
            file_copy_log.write(f"Destination directory {destination_directory} is empty. Copying root directory.\n")
            shutil.copytree(source_directory, destination_directory)
            print(f"Root directory copied to {destination_directory}.")
            file_copy_log.write(f"Root directory copied to {destination_directory}.\n")

def main():
    with open("config.json", "r") as f:
        config_data = json.load(f)
        config = Config(
            config_data["source_directory"],
            config_data["destination_directory"],
            config_data["file_string"],
            config_data["max_files"],
            config_data["max_files_value"]
        )

    current_month_day = datetime.datetime.now().strftime("%m%d")
    log_file_name = f"{current_month_day}_log.txt"

    logger = setup_logger(log_file_name)
    copy_files(config, logger)

if __name__ == "__main__":
    main()
