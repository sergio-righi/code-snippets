import os
import requests
from bson import ObjectId

# Function to download an image and save it
def download_image(url, save_path):
    try:
        # Adding headers to simulate a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Get image from the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors

        # Check if the content is an image by inspecting the Content-Type header
        content_type = response.headers['Content-Type']
        
        if 'image' in content_type:
            # Save the image
            with open(save_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f'Skipped (not an image): {url}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to download {url}: {e}')


# Function to process a .txt file, download images and store them in the proper folder
def process_txt_file(txt_file_path, output_directory):
    # Get the base name (without extension) of the txt file to use as folder name
    file_name = os.path.splitext(os.path.basename(txt_file_path))[0]
    
    # Create a directory with the same name as the txt file
    file_directory = os.path.join(output_directory, file_name)
    os.makedirs(file_directory, exist_ok=True)
    
    # Read URLs from the txt file
    with open(txt_file_path, 'r') as f:
        urls = f.readlines()
    
    # Loop through the URLs and download each image
    for url in urls:
        url = url.strip()
        if url:  # Skip empty lines
            # Generate a unique Object ID (UUID) for the image file name
            object_id = str(ObjectId())
            file_extension = 'jpeg'
            image_name = f'{object_id}.{file_extension}'
            image_path = os.path.join(file_directory, image_name)
            
            # Download and save the image
            download_image(url, image_path)

# Main function to process all .txt files in the folder
def process_dir(input_directory, output_directory):
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Scan through all .txt files in the folder
    for file_name in os.listdir(input_directory):
        if file_name.endswith('.txt'):
            txt_file_path = os.path.join(input_directory, file_name)
            process_txt_file(txt_file_path, output_directory)

if __name__ == '__main__':
    
    # Set the input directory where .txt files are located and the output directory
    input_dir = '<source_path>'  # Path to directory with .txt files
    output_dir = '<destination_path>'  # Path to output directory where images will be saved
    
    # Process the directory
    process_dir(input_dir, output_dir)
