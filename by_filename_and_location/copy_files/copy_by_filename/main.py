# main.py

import json
from prepare_queue import prepare_queue
from copy_files import copy_files

def main():
    with open("config.json", "r") as f:
        config_data = json.load(f)
    
    prepare_queue(config_data)
    copy_files()

if __name__ == "__main__":
    main()
