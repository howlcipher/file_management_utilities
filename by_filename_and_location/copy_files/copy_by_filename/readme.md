# copy_by_filename.py

This Python script is designed to copy files from a source directory to a destination directory based on specified conditions.

## Description

The script reads configuration settings from a `config.json` file, including the source directory, destination directory, and a list of strings to match in file names. It then traverses the source directory, matches files based on the specified conditions, and copies the matched files to the destination directory.

## Features

- Copy files based on matching file names.
- Limit the number of files to copy.
- Log file copying process with detailed information.

## Usage

1. **Install Dependencies**: Ensure you have Python installed on your system.
2. **Configuration**: Edit the `config.json` file to specify your source and destination directories, strings to match in file names, and maximum number of files to copy.
3. **Run the Script**: Execute the script by running `python copy_by_filename.py`.

## Configuration

The `config.json` file contains the following parameters:

- `source_directory`: Path to the source directory containing files to copy.
- `destination_directory`: Path to the destination directory where files will be copied.
- `file_string`: List of strings to match in file names.
- `max_files`: Boolean flag indicating whether to limit the number of files copied.
- `max_files_value`: Maximum number of files to copy.

## Logging

The script logs the file copying process to a log file in the format `MMDD_log.txt` in the current working directory.

## Example Configuration

Here is an example `config.json`:

```json
{
    "source_directory": "path/to/source",
    "destination_directory": "path/to/destination",
    "file_string": ["string1", "string2", "string3"],
    "max_files": true,
    "max_files_value": 10
}
