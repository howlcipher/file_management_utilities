import os
import json
import logging
import datetime

class Config:
    def __init__(self, destination_directory, first_string, second_string):
        self.destination_directory = destination_directory
        self.first_string = first_string
        self.second_string = second_string

def setup_logger(log_file_name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

def delete_files(config, logger):
    destination_directory = config.destination_directory
    first_string = config.first_string
    second_string = config.second_string

    files_deleted = 0
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    delete_log_name = f"{current_date}_file_delete_log.txt"

    with open(delete_log_name, 'a+') as delete_log:
        for root, dirs, files in os.walk(destination_directory):
            for file in files:
                file_path = os.path.join(root, file)
                if all(substring in file for substring in first_string) and second_string in file:
                    try:
                        os.remove(file_path)
                        files_deleted += 1
                        logger.info(f"Deleted file: {file_path}")
                        delete_log.write(f"Deleted file: {file_path}\n")
                    except Exception as e:
                        logger.error(f"Error deleting file {file_path}: {e}")
                        delete_log.write(f"Error deleting file {file_path}: {e}\n")

        logger.info(f"Total files deleted: {files_deleted}")
        delete_log.write(f"Total files deleted: {files_deleted}\n")

def main():
    with open("config.json", "r") as f:
        config_data = json.load(f)
        config = Config(
            config_data["destination_directory"],
            config_data["first_string"],
            config_data["second_string"]
        )

    current_month_day = datetime.datetime.now().strftime("%m%d")
    log_file_name = f"{current_month_day}_log.txt"

    logger = setup_logger(log_file_name)
    delete_files(config, logger)

if __name__ == "__main__":
    main()
