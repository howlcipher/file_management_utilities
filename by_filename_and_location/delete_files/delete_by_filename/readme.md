# delete_by_file_name.py

This Python script is designed to delete files from a specified destination directory based on certain criteria.

## Prerequisites

- Python 3.x
- JSON module (usually comes pre-installed with Python)

## Configuration

Before running the script, you need to provide configuration parameters in a `config.json` file:

```json
{
  "destination_directory": "/path/to/your/destination/directory",
  "first_string": ["string1", "string2"],
  "second_string": "string3"
}
```
- destination_directory: The path to the destination directory from which files will be deleted.
- first_string (optional): A list of strings that must be present in the filenames for deletion.
- second_string (optional): A string that must be present in the filenames for deletion.