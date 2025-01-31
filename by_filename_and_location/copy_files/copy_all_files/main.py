from prepare_queue import FileQueuePreparer
from copy_files import FileCopier

def main():
    config_file = 'config.json'

    # Prepare the file queue
    file_queue_preparer = FileQueuePreparer(config_file)
    file_queue_preparer.run()
    print("File queue preparation completed.")

    # Copy the files
    file_copier = FileCopier()
    file_copier.copy_files()
    print("File copying process completed.")

if __name__ == '__main__':
    main()
