# Extract Matching Lines
This script extracts lines from a text file based on a keyword and regex pattern defined in a configuration file (config.json). It searches for lines starting with a number after encountering a specified keyword.

## Configuration
The configuration for the script is stored in a config.json file. Below is an example configuration:

### config.json

    {
        "input_file": "input.txt",
        "output_file": "output.txt",
        "keyword": "Files copied for each file string:",
        "regex_pattern": "^\\d+:\\s*\\d+$"
    }
- input_file: Path to the input text file.
- output_file: Path to the output text file where matched lines will be saved.
- keyword: The keyword after which lines will be considered for extraction.
- regex_pattern: The regex pattern to match lines. Lines matching this pattern will be extracted.
## Requirements
- Python 3.x
## Usage
- Create a config.json file with the desired configuration.
- Place the input text file at the location specified in the config.json.
- Run the script extractor.py.

## Running the Script
    python extractor.py