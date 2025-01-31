import os
import random
import datetime
import shutil
import json
import asyncio
from concurrent.futures import ProcessPoolExecutor

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

destination_directory = config["destination_directory"]
file_strings = config["file_strings"]
additional_string = config.get("additional_string", "_STA")
file_type = config.get("file_type", ".pdf")
months_ago = config.get("months_ago", 12)

# Helper function to generate a random date within a specific month
def random_day_in_month(year, month):
    start_date = datetime.date(year, month, 1)
    if month == 12:
        end_date = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
    random_day = random.randint(1, (end_date - start_date).days + 1)
    return datetime.date(year, month, random_day)

# Function to create a single file
def create_file(file_string, target_date):
    try:
        random_date = random_day_in_month(target_date.year, target_date.month)
        filename = f"{file_string}_{random_date.strftime('%m%d%Y')}{additional_string}{file_type}"
        file_path = os.path.join(destination_directory, filename)

        # Create a fake PDF (normally you would generate or format the actual content)
        with open(file_path, 'w') as f:
            f.write(f"This is a fake PDF file named {filename}.")

        print(f"Created file: {file_path}")
    except Exception as e:
        print(f"Failed to create file: {file_path}, Error: {e}")

# Main function to create files using multiprocessing and asyncio
async def main():
    today = datetime.date.today()
    months_range = list(range(months_ago))  # Number of months to go back

    # Number of processes for multiprocessing
    num_processes = min(len(file_strings), os.cpu_count())  # Use fewer processes if fewer file_strings than CPU cores

    # Split file creation tasks into batches
    batches = []
    for file_string in file_strings:
        batch_dates = [today - datetime.timedelta(days=i*30) for i in months_range]
        batches.append((file_string, batch_dates))

    # Use ProcessPoolExecutor to handle multiprocessing tasks
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        loop = asyncio.get_event_loop()
        await asyncio.gather(*[loop.run_in_executor(executor, create_files_batch_sync, batch) for batch in batches])

    print("File creation complete.")

# Synchronous function to handle batch file creation
def create_files_batch_sync(batch):
    file_string, target_dates = batch
    for target_date in target_dates:
        create_file(file_string, target_date)

if __name__ == "__main__":
    asyncio.run(main())
