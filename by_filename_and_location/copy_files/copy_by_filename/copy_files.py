# copy_files.py

import os
import shutil
import sqlite3

def copy_files():
    conn = sqlite3.connect('file_copy_queue.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, src_file, dst_file FROM file_queue WHERE status = "pending"')
    rows = cursor.fetchall()

    for row in rows:
        id, src_file, dst_file = row
        try:
            shutil.copy(src_file, dst_file)
            cursor.execute('UPDATE file_queue SET status = "copied" WHERE id = ?', (id,))
        except Exception as e:
            print(f"Error copying {src_file}: {e}")
            cursor.execute('UPDATE file_queue SET status = "error" WHERE id = ?', (id,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    copy_files()
