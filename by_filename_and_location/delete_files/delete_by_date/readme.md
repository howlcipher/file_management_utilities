# Delete Files by Date Script

This Python script deletes any files and subdirectories created on a specific date, as configured in a `config.json` file.

## Overview

The script reads a configuration file (`config.json`) to get the target directory and the date. It then iterates through the files and subdirectories, checking their creation dates, and deletes any that were created on the specified date.

## Configuration

Create a `config.json` file in the same directory as the script with the following structure:

    
    {
    "target_directory": "/path/to/your/directory",
    "target_date": "2024-06-19"
    }

- target_directory: The directory where the script will look for files and subdirectories to delete.
- target_date: The date on which the files and subdirectories were created, in the format YYYY-MM-DD.

## Usage

1. Ensure you have Python installed on your system.
2. Place the delete_files_by_date.py script and the config.json file in the same directory.
3. Update the config.json file with your target directory and date.
4. Run the script: `python delete_by_date.py`

## Notes
- Safety Check: The script uses os.path.getctime() to get the creation date of files and directories. This function may behave differently on different operating systems. For example, on Unix-based systems, it may return the last metadata change time instead of the creation time.
- Dry Run: It is recommended to perform a dry run by modifying the script to only log the files and directories it would delete, without actually deleting them. This ensures you can review the actions before committing to them.
- Error Handling: For a production-ready script, consider adding error handling to manage permissions issues or read/write errors.
## Example
Here is an example config.json file:

    {
    "target_directory": "/Users/yourname/Documents/test_directory",
    "target_date": "2024-06-19"
    }

Running the script with this configuration will delete any files and subdirectories created on June 19, 2024, within /Users/yourname/Documents/test_directory.