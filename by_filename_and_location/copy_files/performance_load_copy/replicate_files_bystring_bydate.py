import os
import shutil
import json
from datetime import datetime, timedelta

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def find_file(source_directory, search_string):
    for f in os.listdir(source_directory):
        if search_string in f:
            return f
    return None

def copy_and_rename_file(file, source_directory, target_directory, base_date, search_string, copies, log_file):
    current_date = datetime.strptime(base_date, "%m%d%Y")
    date_increment = timedelta(days=1)
    
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    copied_count = 0

    for _ in range(copies):
        base_name, ext = os.path.splitext(file)
        parts = base_name.split("_")
        if len(parts) > 1:
            new_name = f"{parts[0]}_{current_date.strftime('%m%d%Y')}_{search_string}{ext}"
            current_date += date_increment
            source_path = os.path.join(source_directory, file)
            target_path = os.path.join(target_directory, new_name)
            shutil.copy2(source_path, target_path)
            log_message = f"Copied {source_path} to {target_path}"
            print(log_message)
            log_file.write(log_message + "\n")
            copied_count += 1
    
    return copied_count

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%m%d%Y")
        return True
    except ValueError:
        return False

def main():
    config_path = 'config.json'
    log_directory = "logs"
    today = datetime.now().strftime("%Y%m%d")
    log_path = os.path.join(log_directory, f"log_{today}.txt")

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    with open(log_path, 'a') as log_file:
        config = load_config(config_path)
        source_directory = config['source_directory']
        target_directory = config['target_directory']
        base_date = config['base_date']
        
        if not is_valid_date(base_date):
            print("Error: Invalid base date format. Please use MMDDYYYY format.")
            return

        strings_to_search = config['strings_to_search']

        for item in strings_to_search:
            search_string = item['string']
            copies = item['copies']
            base_date_dt = datetime.strptime(base_date, "%m%d%Y")  # Initialize base date for each string iteration
            file = find_file(source_directory, search_string)
            if file:
                for i in range(copies):
                    if i != 0:  # Check if it's not the first iteration
                        new_month = (base_date_dt.month % 12) + 1
                        new_year = base_date_dt.year + ((base_date_dt.month + 1) // 13)  # Increment year only if month goes from December to January
                        base_date_dt = base_date_dt.replace(month=new_month, year=new_year)
                    base_date_str = base_date_dt.strftime("%m%d%Y")
                    copied_count = copy_and_rename_file(file, source_directory, target_directory, base_date_str, search_string, 1, log_file)
                    log_message = f"Copied file for string '{search_string}' with base date: {base_date_str}"
                    print(log_message)
                    log_file.write(log_message + "\n")
            else:
                log_message = f"No files found for string '{search_string}'"
                print(log_message)
                log_file.write(log_message + "\n")

if __name__ == "__main__":
    main()
