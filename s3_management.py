import os
import bson
import boto3
from botocore.exceptions import NoCredentialsError
from bson import ObjectId

# Tebi Cloud configuration
ACCESS_KEY = '<access_key>'
SECRET_KEY = '<secret_key>'
BUCKET_NAME = '<bucket_name>'

# Initialize the S3 client (S3 API compatible)
s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url='https://s3.tebi.io'  # Replace with Tebi's endpoint
)

def is_valid_objectid(filename):
    """Check if the filename (without extension) is a valid MongoDB ObjectId."""
    name, _ = os.path.splitext(filename)  # Remove the file extension
    try:
        ObjectId(name)  # Validate if the name can be an ObjectId
        return True
    except bson.errors.InvalidId:
        return False
      
      
def file_exists(bucket_name, file_key):
    """Check if the file already exists in the bucket."""
    try:
        s3_client.head_object(Bucket=bucket_name, Key=file_key)
        print(f'File {file_key} already exists, skipping upload.')
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise e
          
          
def upload_files(directory, bucket_name):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)

            # Check if the filename is a valid MongoDB ObjectId
            if not is_valid_objectid(file):
                # Generate a new ObjectId and rename the file
                new_filename = f'{ObjectId()}{os.path.splitext(file)[1]}'  # Retain original extension
                new_file_path = os.path.join(root, new_filename)
                os.rename(file_path, new_file_path)
                file_path = new_file_path  # Update the path to the new file
                relative_path = os.path.relpath(new_file_path, directory)
                print(f'Renamed {file} to {new_filename}')

            # Check if the file already exists in the bucket
            if not file_exists(bucket_name, relative_path):
                try:
                    s3_client.upload_file(file_path, bucket_name, relative_path)
                    print(f'Uploaded: {relative_path}')
                except NoCredentialsError:
                    print('Credentials not available')
                except Exception as e:
                    print(f'Failed to upload {file_path}: {e}')


def download_all_files(target_dir, bucket_name):
    """Download all files from the bucket, preserving the directory structure."""

    # List directories
    response_root = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter="/")
    
    if 'CommonPrefixes' not in response_root:
        print("No directories found in the bucket.")
        return

    for directory in response_root['CommonPrefixes']:
        
        # List objects        
        response_directory = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=directory['Prefix'])
        
        if 'Contents' not in response_directory:
            print("No files found in the bucket.")
            return
        
        for document in response_directory['Contents'][1:]:
            file_key = document['Key']  # This includes the full path in the bucket

            # Create the local directory structure
            local_file_path = os.path.join(target_dir, file_key)
            target_dir_path = os.path.dirname(local_file_path)

            if not os.path.exists(target_dir_path):
                os.makedirs(target_dir_path)

            # Download the file
            try:
                print(f'Downloading {file_key} to {local_file_path}...')
                s3_client.download_file(bucket_name, file_key, local_file_path)
            except NoCredentialsError:
                print('Credentials not available.')
            except Exception as e:
                print(f'Error downloading {file_key}: {e}')


def delete_all_files(bucket_name):
    try:
        # List all objects in the bucket
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                print(f'Deleting: {obj["Key"]}')
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f'All files deleted from bucket "{bucket_name}"')
        else:
            print(f'No files found in bucket "{bucket_name}"')
    except NoCredentialsError:
        print('Credentials not available')
    except Exception as e:
        print(f'Failed to delete files: {e}')


if __name__ == '__main__':
    target_dir = '<target_path>'
    upload_files(target_dir, BUCKET_NAME)
    # delete_all_files(BUCKET_NAME)
    # download_all_files(target_dir, BUCKET_NAME)
