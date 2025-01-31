import json
import os
import shutil
import datetime

class Config:
    def __init__(self, source_directory, destination_root, month_years):
        self.source_directory = source_directory
        self.destination_root = destination_root
        self.month_years = month_years

def copy_files_to_folders(source_directory, destination_root, month_years, log_file):
    if not os.path.exists(source_directory):
        log_message = f"Source directory '{source_directory}' does not exist. Skipping..."
        print(log_message)
        log_to_file(log_message, log_file)
        return

    total_files_found = 0
    total_files_copied = 0

    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            source_path = os.path.join(root, filename)

            if os.path.isfile(source_path):
                try:
                    folder_name = filename.split('_')[0]  # Get the folder name from the filename

                    # Get the year from the filename
                    year = filename.split('_')[2].split('-')[1][:4]
                    month =filename.split('_')[2].split('-')[0]
                    month_year = f"{month}-{year}"
                except:
                    print(f"folder name is not the correct structure '{folder_name}'")
                    continue
                # Check if the file's month-year is in the list of allowed month-years
                if month_year not in month_years:
                    print(f"Skipping file '{filename}' with month-year '{month_year}'")
                    continue  # Skip processing this file if its month-year is not in the list

                total_files_found += 1

                destination_directory = os.path.join(destination_root, folder_name, 'Statements', year)
                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)

                destination_path = os.path.join(destination_directory, filename)

                # Check if the file already exists in the destination
                if not os.path.exists(destination_path):
                    try:
                        shutil.copy(source_path, destination_path)
                        total_files_copied += 1
                        log_message = f"File '{filename}' copied to folder '{folder_name}' in {destination_path}"
                        print(log_message)
                        log_to_file(log_message, log_file)
                    except Exception as e:
                        log_message = f"Error copying file '{filename}': {e}"
                        print(log_message)
                        log_to_file(log_message, log_file)
                else:
                    log_message = f"File '{filename}' already exists in the destination folder '{destination_directory}'"
                    print(log_message)
                    log_to_file(log_message, log_file)

    log_message = f"Total files found: {total_files_found}, Total files copied: {total_files_copied}"
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
        config = Config(config_data["sourceDirectory"], config_data["destinationRoot"], config_data["monthYears"])

    current_month_day = datetime.datetime.now().strftime("%m%d")
    log_file_name = f"{current_month_day}_log.txt"
    log_file_path = os.path.join("logs", log_file_name)

    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Loop over all month-years specified in the config
    for month_year in config.month_years:
        month, year = month_year.split('-')
        source_directory = config.source_directory.replace('${month}', f"{int(month):02d}")
        copy_files_to_folders(source_directory, config.destination_root, month_year, log_file_path)

    add_timestamp_separator(log_file_path)

if __name__ == "__main__":
    main()
