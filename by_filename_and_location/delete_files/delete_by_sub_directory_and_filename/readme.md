# delete_by_sub_directory_and_filename.py

This Python script is designed to delete files from a specified directory based on certain conditions.

## Features

- Deletes files from the destination directory that match specified criteria.
- Logs the deletion process to a log file with a timestamp.
- Allows configuration of deletion criteria via a JSON configuration file.

## Prerequisites

- Python 3.x installed on your system.
- A valid `config.json` file containing the deletion configuration.

## Usage

1. Ensure you have Python installed on your system.
2. Create a `config.json` file with the following structure:

```json
{
  "destination_directory": "/path/to/destination/directory",
  "first_string": ["string1", "string2"],
  "second_string": "string_to_match"
}
