import os
import json
import logging
import sqlite3
from datetime import datetime

class ConfigLoader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.source_directory = None
        self.destination_directory = None
        self.limit_files = None
        self.file_limit = None
        self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        self.source_directory = config['source_directory']
        self.destination_directory = config['destination_directory']
        self.limit_files = config['limit_files']
        self.file_limit = config['file_limit']

class LoggerSetup:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        today = datetime.now().strftime('%Y-%m-%d')
        log_filename = f'file_queue_{today}.txt'
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

class DatabaseSetup:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.setup_db()

    def setup_db(self):
        self.conn = sqlite3.connect('file_copy_queue.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                src_file TEXT UNIQUE,
                dst_file TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        self.conn.commit()

    def add_to_queue(self, src_file, dst_file):
        try:
            self.cursor.execute('INSERT OR IGNORE INTO file_queue (src_file, dst_file) VALUES (?, ?)', (src_file, dst_file))
            self.conn.commit()
        except Exception as e:
            logging.error(f'Error adding file to queue {src_file}: {e}')
            print(f'Error adding file to queue {src_file}: {e}')

class FileQueuePreparer:
    def __init__(self, config_file):
        self.config = ConfigLoader(config_file)
        LoggerSetup()
        self.db = DatabaseSetup()

    def prepare_queue(self):
        file_count = 0
        for entry in os.scandir(self.config.source_directory):
            if entry.is_dir():
                for subdir_entry in os.scandir(entry.path):
                    if subdir_entry.is_file():
                        if self.config.limit_files and file_count >= self.config.file_limit:
                            return
                        src_file = subdir_entry.path
                        rel_path = os.path.relpath(src_file, self.config.source_directory)
                        dst_file = os.path.join(self.config.destination_directory, rel_path)
                        self.db.add_to_queue(src_file, dst_file)
                        file_count += 1

    def run(self):
        self.prepare_queue()


# Usage example:
if __name__ == '__main__':
    config_file = 'config.json'
    file_queue_preparer = FileQueuePreparer(config_file)
    file_queue_preparer.run()
