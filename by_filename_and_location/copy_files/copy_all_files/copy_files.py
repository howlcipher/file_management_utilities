import os
import shutil
import logging
from datetime import datetime
import multiprocessing
import sqlite3

class LoggerSetup:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        today = datetime.now().strftime('%Y-%m-%d')
        log_filename = f'file_copy_{today}.txt'
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

class DatabaseSetup:
    def __init__(self):
        self.db_path = 'file_copy_queue.db'
        self.setup_db()

    def setup_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                src_file TEXT UNIQUE,
                dst_file TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        conn.commit()
        conn.close()

    def get_pending_files(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT src_file, dst_file FROM file_queue WHERE status="pending"')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def update_file_status(self, src_file, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE file_queue SET status = ? WHERE src_file = ?', (status, src_file))
        conn.commit()
        conn.close()

class FileCopier:
    def __init__(self):
        LoggerSetup()
        self.db = DatabaseSetup()

    def copy_file(self, src_file, dst_file):
        try:
            if not os.path.exists(dst_file):
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
                logging.info(f'File copied: {src_file} to {dst_file}')
                print(f'File copied: {src_file} to {dst_file}')
                self.db.update_file_status(src_file, 'completed')
                return True
            else:
                logging.info(f'File already exists and was not copied: {dst_file}')
                print(f'File already exists and was not copied: {dst_file}')
                self.db.update_file_status(src_file, 'exists')
                return False
        except Exception as e:
            logging.error(f'Error copying {src_file} to {dst_file}: {e}')
            print(f'Error copying {src_file} to {dst_file}: {e}')
            self.db.update_file_status(src_file, 'error')
            return False

    def copy_files(self):
        try:
            print("Fetching files to copy from the database.")

            # Fetch pending files from the queue
            tasks = self.db.get_pending_files()
            print(f"Total files to copy: {len(tasks)}")

            # Copy files using multiprocessing
            with multiprocessing.Pool() as pool:
                pool.starmap(self.worker_copy_file, tasks)
                print("Started multiprocessing for file copying.")

            print("Waiting for all processes to complete...")
            pool.close()
            pool.join()

            print("All processes completed.")
            print("Copy process completed.")
        except Exception as e:
            logging.error(f'Error in copy_files function: {e}')
            print(f'Error in copy_files function: {e}')

    def worker_copy_file(self, src_file, dst_file):
        db = DatabaseSetup()  # Create a new database connection in each worker
        try:
            if not os.path.exists(dst_file):
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
                logging.info(f'File copied: {src_file} to {dst_file}')
                print(f'File copied: {src_file} to {dst_file}')
                db.update_file_status(src_file, 'completed')
                return True
            else:
                logging.info(f'File already exists and was not copied: {dst_file}')
                print(f'File already exists and was not copied: {dst_file}')
                db.update_file_status(src_file, 'exists')
                return False
        except Exception as e:
            logging.error(f'Error copying {src_file} to {dst_file}: {e}')
            print(f'Error copying {src_file} to {dst_file}: {e}')
            db.update_file_status(src_file, 'error')
            return False

# Usage example:
if __name__ == '__main__':
    file_copier = FileCopier()
    file_copier.copy_files()
