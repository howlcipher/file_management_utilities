import os
import random
import datetime
import json
import sqlite3

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    print("Configuration loaded successfully:")
    print(json.dumps(config, indent=4))

destination_directory = config["destination_directory"]
file_strings = config["file_strings"]
max_files = config.get("max_files", False)
max_files_value = config.get("max_files_value", 10)
months_ago = config.get("months_ago", 7)
additional_string = config.get("additional_string", "_STA")
file_type = config.get("file_type", ".pdf")

# Helper function to generate a random date within a specific month
def random_day_in_month(year, month):
    start_date = datetime.date(year, month, 1)
    if month == 12:
        end_date = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
    random_day = random.randint(1, (end_date - start_date).days + 1)
    return datetime.date(year, month, random_day)

# Connect to SQLite database
conn = sqlite3.connect('file_copy_queue.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS file_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_string TEXT,
        dst_file TEXT UNIQUE,
        status TEXT DEFAULT 'pending'
    )
''')

# Create file records
total_files_created = 0
today = datetime.date.today()
months_range = list(range(months_ago))

if max_files and max_files_value < months_ago * len(file_strings):
    # Select random months within the range
    selected_months = random.sample(months_range, max_files_value // len(file_strings))
else:
    # Use all months in the range
    selected_months = months_range

for file_string in file_strings:
    for i in selected_months:
        target_date = today - datetime.timedelta(days=i*30)
        random_date = random_day_in_month(target_date.year, target_date.month)
        filename = f"{file_string}_{random_date.strftime('%m%d%Y')}{additional_string}{file_type}"
        dst_file = os.path.join(destination_directory, filename)
        
        # Insert record into the database
        cursor.execute('''
            INSERT OR IGNORE INTO file_queue (file_string, dst_file)
            VALUES (?, ?)
        ''', (file_string, dst_file))
        
        total_files_created += 1

# Commit and close the database connection
conn.commit()
conn.close()

print(f"File records creation complete. Total files created: {total_files_created}")
