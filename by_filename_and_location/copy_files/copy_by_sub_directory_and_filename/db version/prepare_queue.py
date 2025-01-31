import os
import json
import sqlite3

def prepare_queue(config_data):
    conn = sqlite3.connect('file_copy_queue_no_folder.db')
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

    # Extract relevant substrings from file_strings
    trimmed_strings = [s[7:14] for s in file_strings]

    batch_size = 100  # Define a batch size for inserts
    insert_statements = []

    for root, dirs, files in os.walk(source_directory):
        # Filter directories to process
        filtered_dirs = [d for d in dirs if any(trimmed in d for trimmed in trimmed_strings)]
        
        for d in filtered_dirs:
            folder_path = os.path.join(root, d)
            match_found = False
            for dir_root, _, dir_files in os.walk(folder_path):
                for filename in dir_files:
                    file_path = os.path.join(dir_root, filename)
                    for s in file_strings:
                        if s in filename:
                            match_found = True
                            try:
                                # Construct destination path
                                relative_path = os.path.relpath(file_path, source_directory)
                                destination_path = os.path.join(destination_directory, relative_path)

                                # Add the insert statement to the list
                                insert_statements.append((file_path, destination_path, 'pending'))

                                # Insert in batches
                                if len(insert_statements) >= batch_size:
                                    cursor.executemany('''
                                        INSERT INTO file_queue (src_file, dst_file, status)
                                        VALUES (?, ?, ?)
                                    ''', insert_statements)
                                    conn.commit()
                                    insert_statements = []  # Clear the list after inserting
                            except sqlite3.IntegrityError:
                                print(f"Warning: Duplicate entry for {file_path}. Skipping.")
            
            if match_found:
                print(f"Match found in directory: {folder_path}")
            else:
                print(f"No match found in directory: {folder_path}")
    
    # Insert any remaining records
    if insert_statements:
        cursor.executemany('''
            INSERT INTO file_queue (src_file, dst_file, status)
            VALUES (?, ?, ?)
        ''', insert_statements)
        conn.commit()
    
    conn.close()

if __name__ == "__main__":
    with open("config.json", "r") as f:
        config_data = json.load(f)
    
    prepare_queue(config_data)
