import json
import os
import shutil
import datetime

class Config:
    def __init__(self, destination_root, month_years):
        self.destination_root = destination_root
        self.month_years = month_years

def delete_files_from_folders(config, log_file):
    if not os.path.exists(config.destination_root):
        log_message = f"Destination root directory '{config.destination_root}' does not exist. Exiting..."
        print(log_message)
        log_to_file(log_message, log_file)
        return

    total_files_deleted = 0

    for month_year in config.month_years:
        month, year = month_year.split('-')
        destination_directory = os.path.join(config.destination_root, 'Statements', year)

        if not os.path.exists(destination_directory):
            log_message = f"Destination directory for {month_year} does not exist. Skipping..."
            print(log_message)
            log_to_file(log_message, log_file)
            continue

        try:
            shutil.rmtree(destination_directory)
            total_files_deleted += 1
            log_message = f"All files in folder for {month_year} deleted successfully."
            print(log_message)
            log_to_file(log_message, log_file)
        except Exception as e:
            log_message = f"Error deleting files for {month_year}: {e}"
            print(log_message)
            log_to_file(log_message, log_file)

    log_message = f"Total files deleted: {total_files_deleted}"
    print(log_message)
    log_to_file(log_message, log_file)

def log_to_file(log_message, log_file_path):
    with open(log_file_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(timestamp + " " + log_message + "\n")

def add_timestamp_separator(log_file_path):
    timestamp_separator = f"----- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----"
    with open(log_file_path, "a") as f:
        f.write("\n" + timestamp_separator + "\n")

def main():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        config = Config(config_data["destinationRoot"], config_data["monthYears"])

    current_month_day = datetime.datetime.now().strftime("%m%d")
    log_file_name = f"{current_month_day}_delete_log.txt"
    log_file_path = os.path.join("logs", log_file_name)

    if not os.path.exists("logs"):
        os.makedirs("logs")

    delete_files_from_folders(config, log_file_path)

    add_timestamp_separator(log_file_path)

if __name__ == "__main__":
    main()
