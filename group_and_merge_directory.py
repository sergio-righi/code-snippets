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

if __name__ == '__main__':
    
    input_folder = ''

    # Process the folder
    merge_files(input_folder)
