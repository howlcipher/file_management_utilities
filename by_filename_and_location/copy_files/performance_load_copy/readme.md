# Replicate Files Script

This Python script copies and renames files from a source directory based on specified strings. The script searches for files containing specific strings and copies them a specified number of times, appending a date and the search string to the file names. The script logs its operations to a dated log file.

## Requirements

- Python 3.x

## Installation

1. Clone or download this repository.
2. Ensure you have Python 3.x installed on your machine.

## Configuration

Create a `config.json` file in the same directory as the script with the following structure:

```json
{
    "source_directory": "path/to/source/directory",
    "target_directory": "path/to/target/directory",
    "base_date": "MMDDYYYY",
    "strings_to_search": [
      {
        "string": "SEARCH_STRING_1",
        "copies": NUMBER_OF_COPIES_1
      },
      {
        "string": "SEARCH_STRING_2",
        "copies": NUMBER_OF_COPIES_2
      },
      {
        "string": "SEARCH_STRING_3",
        "copies": NUMBER_OF_COPIES_3
      }
    ]
}

```
- source_directory: Path to the source directory containing files to be copied.
- target_directory: Path to the target directory where files will be copied.
- strings_to_search: List of objects where each object contains:
    - string: The substring to search for in file names.
    - copies: The number of times to copy and rename the matching file.

## Usage
1. Save the script to a file named file_copier.py.
2. Create the config.json file as described above.
3. Run the script using:
```python replicate_files_bystring_bydate```
## Logging
The script logs its operations to a log file located in the logs directory. The log file is named with today's date in the format log_YYYYMMDD.txt.

## Example
Suppose you have the following files in your source directory:

```
example_file_1.pdf
test_file_1.pdf
sample_file_1.pdf
```
And your config.json is configured as follows:
```json
{
    "source_directory": "path/to/source/directory",
    "target_directory": "path/to/target/directory",
    "base_date": "MMDDYYYY",
    "strings_to_search": [
      {
        "string": "SEARCH_STRING_1",
        "copies": NUMBER_OF_COPIES_1
      },
      {
        "string": "SEARCH_STRING_2",
        "copies": NUMBER_OF_COPIES_2
      },
      {
        "string": "SEARCH_STRING_3",
        "copies": NUMBER_OF_COPIES_3
      }
    ]
}

```
When you run the script, the target_directory will contain:

example_01012015_example.pdf
example_02012015_example.pdf
example_03012015_example.pdf
test_01012015_test.pdf
test_02012015_test.pdf
sample_01012015_sample.pdf
## Notes
The script only copies the first file found that matches each search string.
If no files match a search string, a log entry will indicate this.

