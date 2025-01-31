import re
import json

def extract_lines_after_keyword(config_path):
    # Load configuration from the JSON file
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    input_file = config['input_file']
    output_file = config['output_file']
    keyword = config['keyword']
    regex_pattern = config['regex_pattern']
    
    # Compile the regex pattern
    pattern = re.compile(regex_pattern)
    # Flag to start recording lines after the keyword is found
    start_recording = False
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if start_recording:
                # Strip any leading/trailing whitespace from the line
                line = line.strip()
                # Check if the line matches the pattern
                if pattern.match(line):
                    # Write the matching line to the output file
                    outfile.write(line + '\n')
            elif keyword in line:
                # Set the flag to start recording lines after the keyword is found
                start_recording = True

# Usage
config_path = 'config.json'  # Replace with your config file path
extract_lines_after_keyword(config_path)
