import os
import csv
import shutil
import tempfile
import zipfile

# Define the folder containing all main zip files
main_files_folder = 'exel/raw data'

# Define the output CSV file
output_csv_file = 'exel/batched_pulse_data.csv'

# Define the column names
column_names = [
    'TYPE', 'DATE AND TIME', 'Latitude', 'Longitude',
    'peak current', 'reserved', 'height',
    'number of sensors', 'multiplicity'
]

# Function to parse the content of a text file
def parse_text_file(file_path, output_csv_writer):
    with open(file_path, 'r') as txt_file:
        csv_reader = csv.reader(txt_file)
        for row in csv_reader:
            # Check if the row has the expected number of columns
            if len(row) == len(column_names):
                # Check if the first element of the row is '0'
                if row and row[0] == '0':
                    output_csv_writer.writerow(row)
            else:
                print(f"Problematic line found in file: {file_path}")
                print(f"Content of the problematic line: {row}")
                print("Skipping this line.")
                print()

# Initialize the output CSV file with column names
with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(column_names)

    # Set to store processed file paths
    processed_files = set()

    # Iterate over each file in the main files folder
    for file_name in os.listdir(main_files_folder):
        if file_name.endswith('.zip'):
            # Construct the full path to the zip file
            outer_zip_path = os.path.join(main_files_folder, file_name)
            print(outer_zip_path)
            # Check if the file has already been processed
            if outer_zip_path in processed_files:
                continue

            # Create a temporary directory to extract files
            temp_dir = tempfile.mkdtemp()

            # Extract all zip files from the current main zip file
            with zipfile.ZipFile(outer_zip_path, 'r') as outer_zip:
                outer_zip.extractall(path=temp_dir)

                # Iterate over the files in the extracted directory
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.zip'):  # Check if the file is an inner zip
                            inner_zip_path = os.path.join(root, file)
                            print(inner_zip_path)
                            # Extract the inner zip file
                            with zipfile.ZipFile(inner_zip_path, 'r') as inner_zip:
                                inner_zip.extractall(path=temp_dir)

                # Iterate over the files in the extracted directory again
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if root.endswith('pulse') and file.endswith('.txt'):
                            file_path = os.path.join(root, file)
                            # Parse the content of the text file and write to output CSV file
                            parse_text_file(file_path, csv_writer)

            # Add the processed file to the set
            processed_files.add(outer_zip_path)

            # Clean up temporary directory
            shutil.rmtree(temp_dir)

print("CSV file created successfully.")
