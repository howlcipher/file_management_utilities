import json
import os
import shutil
import datetime

# Configuration class to hold source directory, destination root, and desired year
class Config:
    def __init__(self, source_directory, destination_root, desired_year):
        self.source_directory = source_directory  # Path to the source directory
        self.destination_root = destination_root  # Path to the root of the destination directory
        self.desired_year = desired_year  # Desired year for categorizing files

# Function to copy files from the source directory to the destination directory
def copy_files_to_folders(source_directory, destination_root, month, log_file, desired_year):
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        log_message = f"Source directory '{source_directory}' does not exist. Skipping..."
        print(log_message)
        log_to_file(log_message, log_file)
        return

    total_files_found = 0  # Counter for total files found
    total_files_copied = 0  # Counter for total files successfully copied

    # Walk through the source directory
    for root, _, files in os.walk(source_directory):
        for filename in files:
            source_path = os.path.join(root, filename)  # Full path to the source file

            # Ensure the path is a file
            if os.path.isfile(source_path):
                total_files_found += 1  # Increment the found files counter

                # Skip files that do not contain the desired year in the filename
                if desired_year not in filename:
                    log_message = f"Skipping file '{filename}' as it does not contain the desired year '{desired_year}'."
                    print(log_message)
                    log_to_file(log_message, log_file)
                    continue

                # Extract folder name, fallback to 'Unknown' if empty
                folder_name = filename.split('_')[0] if filename.split('_')[0].strip() else 'Unknown'

                # Ensure folder_name is valid
                if not folder_name or folder_name.isspace():
                    folder_name = 'Unknown'

                # Construct the destination directory path
                destination_directory = os.path.join(destination_root, folder_name, 'Statements', desired_year)

                try:
                    # Ensure the destination directory exists
                    os.makedirs(destination_directory, exist_ok=True)

                    # Construct the full path for the destination file
                    destination_path = os.path.join(destination_directory, filename)

                    # Copy the file to the destination directory
                    shutil.copy(source_path, destination_path)
                    total_files_copied += 1  # Increment the copied files counter
                    log_message = f"File '{filename}' copied to folder '{folder_name}' in QA/Statements/{desired_year}."
                    print(log_message)
                    log_to_file(log_message, log_file)
                except Exception as e:
                    # Log any errors encountered during the file copy process
                    log_message = f"Error: {e}"
                    print(log_message)
                    log_to_file(log_message, log_file)

    # Log the summary of the operation
    log_message = f"Total files found: {total_files_found}, Total files copied: {total_files_copied}"
    print(log_message)
    log_to_file(log_message, log_file)

# Function to log messages to a file with a timestamp
def log_to_file(log_message, log_file_path):
    try:
        with open(log_file_path, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(timestamp + " " + log_message + "\n")
    except Exception as e:
        print(f"Failed to write log: {e}")

# Function to add a timestamp separator to the log file
def add_timestamp_separator(log_file_path):
    timestamp_separator = f"----- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----"
    try:
        with open(log_file_path, "a") as f:
            f.write("\n" + timestamp_separator + "\n")
    except Exception as e:
        print(f"Failed to write separator: {e}")

# Main function to execute the file copying process
def main():
    try:
        # Load configuration from the JSON file
        with open('config.json', 'r') as config_file:
            config_data = json.load(config_file)
            config = Config(config_data["sourceDirectory"], config_data["destinationRoot"], config_data["desired_year"])

        print("Running Copy_by_Year.py")
        current_month_day = datetime.datetime.now().strftime("%m%d")  # Get current month and day
        log_file_name = f"{current_month_day}_log.txt"  # Log file name based on current date
        log_file_path = os.path.join("logs", log_file_name)  # Full path to the log file

        # Create the logs directory if it doesn't exist
        if not os.path.exists("logs"):
            os.makedirs("logs")

        # Add a timestamp separator to the log file
        add_timestamp_separator(log_file_path)

        # Iterate over each month
        for month in range(1, 13):
            # Replace the placeholder in the source directory path with the current month
            source_directory = config.source_directory.replace('${month}', f"{month:02d}")
            print(f"Processing month {month}: {source_directory}")
            # Copy files for the current month
            copy_files_to_folders(source_directory, config.destination_root, month, log_file_path, config.desired_year)

        print("Finished Copy_by_Year.py. Check logs for details.")
    except Exception as e:
        print(f"Error in main function: {e}")

# Entry point of the script
if __name__ == "__main__":
    main()
