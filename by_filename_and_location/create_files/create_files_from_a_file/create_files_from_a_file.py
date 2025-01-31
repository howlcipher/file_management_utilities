import os
import shutil
import json
from datetime import datetime, timedelta

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

numbers = config['numbers']
original_file_path = os.path.normpath(config['original_file_path'])
destination_directory = os.path.normpath(config['destination_directory'])

# Debug print statements
print(f"Original file path: {original_file_path}")
print(f"Destination directory: {destination_directory}")

# Check if the original file exists
if not os.path.exists(original_file_path):
    raise FileNotFoundError(f"The original file does not exist: {original_file_path}")

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# Get today's date
today = datetime.now()

# Create copies for the current month and the previous 11 months
for i in range(12):
    month_date = today - timedelta(days=i * 30)  # Roughly 30 days back
    formatted_date = month_date.strftime("%m%d%Y")
    print(f"Date for iteration {i}: {formatted_date}")
    
    for number in numbers:
        new_file_name = f"{number}_{formatted_date}_STA.pdf"
        new_file_path = os.path.normpath(os.path.join(destination_directory, new_file_name))
        
        # Debug print statement for each file operation
        print(f"Attempting to copy {original_file_path} to {new_file_path}")
        
        try:
            # Perform a low-level file copy
            with open(original_file_path, 'rb') as src_file:
                with open(new_file_path, 'wb') as dst_file:
                    shutil.copyfileobj(src_file, dst_file)

            # Verify the file was created
            if os.path.exists(new_file_path):
                print(f"Successfully created: {new_file_path}")
            else:
                print(f"Failed to create: {new_file_path}")
        except shutil.SameFileError:
            print(f"Source and destination represent the same file: {new_file_path}")
        except IsADirectoryError:
            print(f"Destination is a directory: {new_file_path}")
        except PermissionError:
            print(f"Permission denied: {new_file_path}")
        except FileNotFoundError:
            print(f"Source file not found: {original_file_path}")
        except Exception as e:
            print(f"Error copying file to {new_file_path}: {e}")

print("Files copied and renamed successfully.")

# List files in the destination directory for verification
print("Listing files in the destination directory:")
for root, dirs, files in os.walk(destination_directory):
    for file in files:
        print(os.path.join(root, file))
