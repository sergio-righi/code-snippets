import os
import re
from collections import defaultdict

def merge_files(directory):
    # Create a dictionary to group file contents by base name
    files_dict = defaultdict(list)

    # Scan through the directory and categorize files
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            base_name, _ = os.path.splitext(filename)
            # Use regular expression to extract the base name ignoring the suffix (like (1), (2), etc.)
            match = re.match(r'^(.*?)( \(\d+\))?$', base_name)
            if match:
                base_name_key = match.group(1)
                files_dict[base_name_key].append(filename)

    # Process each group of files
    for base_name, files in files_dict.items():
        original_file = None
        numbered_files = []

        # Separate the original file and numbered files
        for file in files:
            if re.search(r'\(\d+\)', file):
                numbered_files.append(file)
            else:
                original_file = file

        # If an original file is found
        if original_file:
            original_file_path = os.path.join(directory, original_file)
            seen_lines = set()  # Set to keep track of unique lines
            temp_lines = []

            # Read existing content of the original file
            if os.path.exists(original_file_path):
                with open(original_file_path, 'r') as infile:
                    for line in infile:
                        if line.strip() and line not in seen_lines:
                            temp_lines.append(line)
                            seen_lines.add(line)

            # Append content from numbered files
            for file in numbered_files:
                file_path = os.path.join(directory, file)
                with open(file_path, 'r') as infile:
                    temp_lines.append("\n")  # Add a newline before each numbered file's content
                    for line in infile:
                        if line.strip() and line not in seen_lines:
                            temp_lines.append(line)
                            seen_lines.add(line)

            # Remove any empty line at the end of the file
            if temp_lines and temp_lines[-1] == "\n":
                temp_lines.pop()
            
            # Write unique lines to the original file
            with open(original_file_path, 'w') as outfile:
                outfile.writelines(temp_lines)

            # Remove the numbered files after merging
            for file in numbered_files:
                os.remove(os.path.join(directory, file))


def move_files(source_dir, destination_dir):
    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Scan the files in the source directory
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        destination_path = os.path.join(destination_dir, filename)

        # Check if it's a file (and not a directory)
        if os.path.isfile(source_path):
            # Move the file to the destination
            os.rename(source_path, destination_path)
            print(f"Moved: {filename}")
        else:
            print(f"Skipped directory: {filename}")
            

if __name__ == '__main__':
    
    input_dir = '<source_path>'
    output_dir = '<destination_path>'

    # Process the folder
    merge_files(input_dir)
    
    # Move files to the target dir
    move_files(input_dir, output_dir)
