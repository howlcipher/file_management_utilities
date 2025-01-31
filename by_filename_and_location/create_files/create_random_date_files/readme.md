# File Management Scripts

This repository contains Python scripts to generate file records and manage file operations using SQLite and Python's standard libraries.

## Scripts

### 1. `prepare_queue.py`

This script generates file records with randomly generated filenames in a specified format and stores them in an SQLite database.

#### Usage

1. **Configuration**
   - Ensure `config.json` is properly configured with the following parameters:
     ```json
     {
       "destination_directory": "/path/to/destination/directory",
       "file_strings": ["file_string_1", "file_string_2", "file_string_3"],
       "max_files": true,
       "max_files_value": 10,
       "months_ago": 7,
       "additional_string": "_STA",
       "file_extension": ".pdf"
     }
     ```
     - `destination_directory`: Destination directory where files will be created.
     - `file_strings`: List of file strings used in generating filenames.
     - `max_files`: Boolean indicating whether to limit the number of files generated.
     - `max_files_value`: Maximum number of files to generate (used if `max_files` is `true`).
     - `months_ago`: Number of months ago to generate random dates within.
     - `additional_string`: Additional string to append to the filename (e.g., "_STA").
     - `file_extension`: File extension for the generated files (e.g., ".pdf").

2. **Execution**
   - Run the script using Python 3:
     ```
     python prepare_queue.py
     ```
   - This script will create a SQLite database (`file_copy_queue.db`) if it doesn't exist, generate file records with unique filenames based on `file_strings`, a random date within the last `months_ago` months, and store them in the database.

### 2. `create.py`

This script reads file records from the SQLite database (`file_copy_queue.db`) and performs file copying operations from a source directory to the destinations specified in the database.

#### Usage

1. **Configuration**
   - Ensure `config.json` and `file_copy_queue.db` are accessible and correctly populated by `prepare_queue.py`.
   
2. **Execution**
   - After `file_copy_queue.db` is populated by `prepare_queue.py`, run `copy_files.py` to copy files based on the queue:
     ```
     python copy_files.py
     ```
   - This script iterates through pending file records in the database, attempts to copy corresponding files from the source directory (`\\\\fifsfiles\\backendimages`) to their respective destinations (`dst_file`), and updates the status in the database to 'copied'.

### Additional Notes

- Modify `prepare_queue.py` and `copy_files.py` as per your specific requirements, such as adjusting filename generation logic, file copying operations, or error handling.
- Ensure Python packages (`sqlite3`, `shutil`, etc.) are installed (`pip install -r requirements.txt`).
