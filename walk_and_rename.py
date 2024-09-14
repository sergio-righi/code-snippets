import os
import bson
from bson.objectid import ObjectId

def is_valid_objectid(file_name):
    """
    Check if the file name is a valid MongoDB ObjectId (excluding extension).
    """
    try:
        ObjectId(file_name)
        return True
    except (bson.errors.InvalidId, TypeError):
        return False


def rename_to_objectid(directory):
    """
    Recursively scans all files in the target directory and renames files 
    to a valid MongoDB ObjectId if their current name is not a valid ObjectId.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            file_path = os.path.join(root, file)
            
            # Check if the current file name (without extension) is a valid ObjectId
            if not is_valid_objectid(file_name):
                # Generate a new ObjectId
                new_file_name = str(ObjectId())
                new_file_path = os.path.join(root, new_file_name + file_ext)
                
                # Rename the file
                os.rename(file_path, new_file_path)
                print(f'Renamed: {file_path} -> {new_file_path}')
            else:
                print(f'Valid ObjectId, no rename needed: {file_path}')

if __name__ == '__main__':
    target_dir = '<target_path>'
    rename_to_objectid(target_dir)
