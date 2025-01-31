import os
import shutil
import sqlite3


# Connect to SQLite database
conn = sqlite3.connect('file_copy_queue.db')
cursor = conn.cursor()

# Fetch pending file records
cursor.execute('''
    SELECT id, dst_file FROM file_queue WHERE status = 'pending'
''')
rows = cursor.fetchall()

# Copy files based on the queue
for row in rows:
    file_id, dst_file = row
    num = 1
    try:
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        
        # Construct source file path
        src_file = os.path.join(os.path.basename(dst_file))
        
        # Create a fake PDF (for demonstration purposes, normally you would copy the actual file)
        with open(src_file, 'w') as f:
            f.write(f"This is a fake PDF file named {os.path.basename(src_file)}.")
        
        # Copy file
        shutil.copy(src_file, dst_file)
        
        # Update status to 'created'
        cursor.execute('''
            UPDATE file_queue SET status = 'created' WHERE id = ?
        ''', (file_id,))
        print(f"Created file: {num} {src_file} to {dst_file}")
        num += 1
    except Exception as e:
        print(f"Failed to copy {src_file} to {dst_file}: {e}")

# Commit and close the database connection
conn.commit()
conn.close()

print("File copying complete.")
