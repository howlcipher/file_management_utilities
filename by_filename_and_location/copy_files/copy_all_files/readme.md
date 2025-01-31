# Copy All Files Script

This Python script copies files and subdirectories from a source directory to a destination directory. It also supports limiting the number of files copied and logs the copy operations.

## Configuration

Create a `config.json` file in the same directory as the script with the following structure:

    {
    "source_directory": "/path/to/source/directory",
    "destination_directory": "/path/to/destination/directory",
    "limit_files": true,
    "file_limit": 100
    }
- source_directory: The directory from which files and subdirectories will be copied.
- destination_directory: The directory to which files and subdirectories will be copied.
- limit_files: A boolean indicating whether to limit the number of files copied.
- file_limit: The maximum number of files to copy if limit_files is set to true.

## Usage
1. Ensure you have Python installed on your system.
2. Place the prepare_queue.py, copy_files.py, and the config.json file in the same directory.
3. Update the config.json file with your desired configuration.
4. Run the script: python main.py

## Logging
The script generates a log file named file_copy_<today's_date>.txt in the same directory as the script. The log file contains information about the directories created and the files copied, as well as any files that already exist in the destination directory.

Example
Here is an example config.json file:

    {
    "source_directory": "/Users/yourname/Documents/source_directory",
    "destination_directory": "/Users/yourname/Documents/destination_directory",
    "limit_files": true,
    "file_limit": 100
    }
    
Running the script with this configuration will copy up to 100 files from /Users/yourname/Documents/source_directory to /Users/yourname/Documents/destination_directory.

## Project Structure
- main.py: Entry point of the script that coordinates the file queue preparation and file copying processes.
- prepare_queue.py: Handles the configuration loading, logging setup, database setup, and preparing the file queue.
- copy_files.py: Handles the actual file copying process using multiprocessing and database management.
- config.json: Configuration file with paths and settings for the script.
## Detailed Steps
1. File Queue Preparation:

- prepare_queue.py reads the configuration from config.json.
- It scans the source directory and adds files to the database queue, respecting the file limit if specified.
2. File Copying:
- copy_files.py reads the pending files from the database queue.
- It uses multiprocessing to copy files from the source to the destination directory, logging each operation.
- The script updates the status of each file in the database after attempting to copy it.
## Requirements
- Python 3.x
- The following Python packages (install using pip install -r requirements.txt):
    - multiprocessing
    - sqlite3
    - logging
    - json
    - shutil