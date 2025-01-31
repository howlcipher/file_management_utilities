# prepare_queue.py

import os
import json
import sqlite3

def prepare_queue(config_data):
    conn = sqlite3.connect('file_copy_queue.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            src_file TEXT UNIQUE,
            dst_file TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')

    source_directory = config_data["source_directory"]
    destination_directory = config_data["destination_directory"]
    file_strings = config_data["file_string"]

    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            for s in file_strings:
                if s in filename:
                    destination_path = os.path.join(destination_directory, os.path.basename(root))
                    try:
                        cursor.execute('''
                            INSERT INTO file_queue (src_file, dst_file, status)
                            VALUES (?, ?, ?)
                        ''', (file_path, destination_path, 'pending'))
                        conn.commit()
                    except sqlite3.IntegrityError:
                        print(f"Warning: Duplicate entry for {file_path}. Skipping.")

    conn.close()

if __name__ == "__main__":
    with open("config.json", "r") as f:
        config_data = json.load(f)
    
    prepare_queue(config_data)
