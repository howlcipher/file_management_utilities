# copy_by_sub_directory_and_filename.py

This Python script is a simple file copy utility designed to copy files from a source directory to a destination directory based on specified conditions.

## Description

The script reads configuration settings from a `config.json` file, including the source directory, destination directory, strings to match in directory names, a string to match in file names, and maximum number of files to copy. It then traverses the source directory, matches directories and files based on the specified conditions, and copies the matched files to the destination directory.

## Features

- Copy files based on matching directory and file names.
- Limit the number of files to copy.
- Log file copying process with detailed information.
- Case-insensitive matching for directory and file names.

## Usage

1. **Install Dependencies**: Ensure you have Python installed on your system.
2. **Configuration**: Edit the `config.json` file to specify your source and destination directories, strings to match in directory names, string to match in file names, and maximum number of files to copy.
3. **Run the Script**: Execute the script by running `python file_copy.py`.

## Configuration

The `config.json` file contains the following parameters:

- `source_directory`: Path to the source directory containing files to copy.
- `destination_directory`: Path to the destination directory where files will be copied.
- `first_string`: List of strings to match in directory names.
- `second_string`: String to match in file names.
- `max_files`: Boolean flag indicating whether to limit the number of files copied.
- `max_files_value`: Maximum number of files to copy.

## Logging

The script logs the file copying process to a log file in the format `YYYY-MM-DD_log.txt` in the current working directory.
