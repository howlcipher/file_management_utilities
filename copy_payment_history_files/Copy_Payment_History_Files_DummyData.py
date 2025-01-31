import os
import json
from datetime import datetime

def load_config():
    # Load configuration from config.json
    with open('config.json') as config_file:
        config = json.load(config_file)
    return config

def get_shaw_acct_number(folder_name):
    # Extracting the account number from the folder name
    parts = folder_name.strip().split('-')
    if len(parts) == 2:
        name, acct_number = parts
        acct_number = acct_number.strip()
        # Formatting the Shaw account number
        shaw_acct_number = f"50000{acct_number}0001"
        return shaw_acct_number
    else:
        return None

def create_blank_pdf(destination_dir, shaw_acct_number, file_name):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Construct the destination file path with the desired naming convention
    destination_path = os.path.join(destination_dir, f"{shaw_acct_number}_{file_name}")

    # Create a blank PDF file
    pdf_content = f"%PDF-1.0\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] >>\nendobj\n4 0 obj\n<< /Type /Font /Subtype /Type1 /Name /F1 /BaseFont /Helvetica /Encoding /MacRomanEncoding >>\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000077 00000 n \n0000000124 00000 n \n0000000174 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n197\n%%EOF"

    # Write the PDF content to the destination file
    with open(destination_path, 'wb') as output_file:
        output_file.write(pdf_content.encode('latin1'))

    print(f"Blank PDF created: {destination_path}")

if __name__ == "__main__":
    # Load configuration
    config = load_config()

    # Set your source and destination directories
    source_directory = config.get('source_directory', '')
    destination_directory = config.get('destination_directory', '')

    if source_directory and destination_directory:
        # Get the current date for logging
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Iterate through the source directory
        for root, dirs, files in os.walk(source_directory):
            for file_name in files:
                # Check if the file ends with "Pymnt History.pdf"
                if file_name.endswith("Pymnt History.pdf"):
                    # Get Shaw account number from the parent folder
                    folder_name = os.path.basename(root)
                    shaw_acct_number = get_shaw_acct_number(folder_name)

                    if shaw_acct_number:
                        # Create blank PDF with the desired naming convention
                        create_blank_pdf(destination_directory, shaw_acct_number, file_name)
    else:
        print("Please provide valid source and destination directories in config.json.")
