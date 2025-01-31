import os
import shutil
import json
import logging
import datetime
import sys

class Config:
    def __init__(self, source_directory, destination_directory, first_string, second_string, max_files, max_files_value):
        self.source_directory = source_directory
        self.destination_directory = destination_directory
        self.first_string = first_string
        self.second_string = second_string
        self.max_files = max_files
        self.max_files_value = max_files_value

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

def copy_files(config, logger):
    source_directory = config.source_directory
    destination_directory = config.destination_directory
    first_strings = config.first_string
    second_string = config.second_string
    max_files = config.max_files
    max_files_value = config.max_files_value

    files_copied = 0
    matched_and_copied = 0  # Initialize the counter
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"{current_date}_log.txt"

    # Set up logging
    logger = setup_logger(log_file_name)

    # Log the start of the process
    logger.info("File copy process started.")
    print("File copy process started.")

    # Log the source directory and destination directory
    logger.info(f"Source Directory: {source_directory}")
    logger.info(f"Destination Directory: {destination_directory}")

    copied_files = set()  # Set to store copied files

    with open(log_file_name, 'a+') as log_file:
        # Check if destination directory exists, create it if not
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        if not os.path.exists(source_directory):
            logger.error(f"Source directory {source_directory} does not exist.")
            print(f"Source directory {source_directory} does not exist.")
            sys.exit(1)  # Exit the application if source directory doesn't exist

        for root, dirs, files in os.walk(source_directory):
            # Filter directories to only include those that match at least one string from the first_string list
            matching_dirs = [d for d in dirs if any(string in d for string in first_strings)]
            dirs[:] = matching_dirs

            for directory in dirs:
                directory_path = os.path.join(root, directory)

                # Check if the directory matches the criteria
                if not any(string in directory for string in first_strings):
                    continue

                file_count = len(os.listdir(directory_path))
                logger.info(f"Traversing directory: {directory_path} - Found {file_count} file(s)")
                print(f"Traversing directory: {directory_path} - Found {file_count} file(s)")

                # Counting and copying matched files in this subdirectory
                matched_files_in_dir = 0
                for filename in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, filename)
                    # Check if the file matches both conditions (case-insensitive)
                    first_string_matched = any(string in filename for string in first_strings)
                    second_string_matched = second_string.lower() in filename.lower()
                    if first_string_matched and second_string_matched:
                        matched_files_in_dir += 1
                        # Get the subdirectory path relative to the source directory
                        rel_path = os.path.relpath(directory_path, source_directory)
                        # Construct the destination directory path
                        dest_dir = os.path.join(destination_directory, rel_path)
                        os.makedirs(dest_dir, exist_ok=True)  # Ensure destination directory exists
                        if file_path not in copied_files:  # Check if file is already copied
                            # Copy the file to the destination directory
                            shutil.copy(file_path, dest_dir)
                            files_copied += 1
                            copied_files.add(file_path)  # Add copied file to the set
                            # Print information only when files are matched and copied
                            matched_string = [string for string in first_strings if string in filename][0]
                            logger.info(f"Copying {file_path} to {dest_dir}, matched string: {matched_string}")
                            print(f"Copying {file_path} to {dest_dir}, matched string: {matched_string}")
                            # Check if the maximum number of files has been reached
                            if max_files and files_copied >= max_files_value:
                                logger.info(f"Max files limit reached. {max_files_value} files copied.")
                                print(f"Max files limit reached. {max_files_value} files copied.")
                                sys.exit()  # Exit the application after reaching the maximum files value
                        else:
                            logger.info(f"File {file_path} already copied.")
                            print(f"File {file_path} already copied.")
                # Check if the maximum number of files has been reached
                if max_files and files_copied >= max_files_value:
                    sys.exit()  # Exit the application after reaching the maximum files value

                logger.info(f"Matched files in {directory_path}: {matched_files_in_dir}")
                print(f"Matched files in {directory_path}: {matched_files_in_dir}")
                matched_and_copied += matched_files_in_dir

        logger.info("All files checked.")
        print("All files checked.")

def main():
    with open("config.json", "r") as f:
        config_data = json.load(f)
        config = Config(
            config_data["source_directory"],
            config_data["destination_directory"],
            config_data["first_string"],
            config_data["second_string"],
            config_data["max_files"],
            config_data["max_files_value"]
        )

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"{current_date}_log.txt"

    logger = setup_logger(log_file_name)
    copy_files(config, logger)

if __name__ == "__main__":
    main()
