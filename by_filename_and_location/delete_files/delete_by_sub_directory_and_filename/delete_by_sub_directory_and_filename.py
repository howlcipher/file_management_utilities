import os
import shutil
import json
import logging
import datetime
import sys

class Config:
    def __init__(self, destination_directory, first_string, second_string):
        self.destination_directory = destination_directory
        self.first_string = first_string
        self.second_string = second_string

def setup_logger(log_file_name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Check if the log file exists
    if os.path.exists(log_file_name):
        file_mode = 'a'  # Append to the existing file
    else:
        file_mode = 'w'  # Create a new file if it doesn't exist

    file_handler = logging.FileHandler(log_file_name, mode=file_mode)
    file_handler.setFormatter(formatter)

    # Add the file handler only if it's not already present
    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger

def delete_files(config, logger):
    destination_directory = config.destination_directory
    first_strings = config.first_string
    second_string = config.second_string

    files_deleted = 0
    matched_and_deleted = 0  # Initialize the counter
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"{current_date}_delete_log.txt"

    # Set up logging
    logger = setup_logger(log_file_name)

    # Log the start of the process
    logger.info("File delete process started.")
    print("File delete process started.")

    # Log the destination directory
    logger.info(f"Destination Directory: {destination_directory}")

    with open(log_file_name, 'a+') as log_file:
        if not os.path.exists(destination_directory):
            logger.error(f"Destination directory {destination_directory} does not exist.")
            print(f"Destination directory {destination_directory} does not exist.")
            sys.exit(1)  # Exit the application if destination directory doesn't exist

        for root, dirs, files in os.walk(destination_directory):
            for directory in dirs:
                directory_path = os.path.join(root, directory)

                # Check if the directory matches the criteria
                if not any(string in directory for string in first_strings):
                    continue

                file_count = len(os.listdir(directory_path))
                logger.info(f"Traversing directory: {directory_path} - Found {file_count} file(s)")
                print(f"Traversing directory: {directory_path} - Found {file_count} file(s)")

                # Counting and deleting matched files in this subdirectory
                matched_files_in_dir = 0
                for filename in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, filename)
                    # Check if the file matches both conditions (case-insensitive)
                    first_string_matched = any(string in filename for string in first_strings)
                    second_string_matched = second_string.lower() in filename.lower()
                    if first_string_matched and second_string_matched:
                        matched_files_in_dir += 1
                        try:
                            os.remove(file_path)
                            files_deleted += 1
                            # Print information only when files are matched and deleted
                            matched_string = [string for string in first_strings if string in filename][0]
                            logger.info(f"Deleting {file_path}, matched string: {matched_string}")
                            print(f"Deleting {file_path}, matched string: {matched_string}")
                        except Exception as e:
                            logger.error(f"Error deleting file {file_path}: {e}")
                            print(f"Error deleting file {file_path}: {e}")
                logger.info(f"Matched files deleted in {directory_path}: {matched_files_in_dir}")
                print(f"Matched files deleted in {directory_path}: {matched_files_in_dir}")
                matched_and_deleted += matched_files_in_dir

        logger.info("All files checked.")
        print("All files checked.")

def main():
    with open("config.json", "r") as f:
        config_data = json.load(f)
        config = Config(
            config_data["destination_directory"],
            config_data["first_string"],
            config_data["second_string"]
        )

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"{current_date}_delete_log.txt"

    logger = setup_logger(log_file_name)
    delete_files(config, logger)

if __name__ == "__main__":
    main()
