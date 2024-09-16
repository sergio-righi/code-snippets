import os
from PIL import Image

# Image optimization settings
MAX_WIDTH = 1920
MAX_HEIGHT = 1080
QUALITY = 80  # Reduce the image quality to

def optimize_image(target_dir):
    """Optimize the image by resizing it and reducing its quality."""
    try:
        with Image.open(target_dir) as img:
            # Convert to RGB if the image is in a non-RGB mode (e.g., P, RGBA)
            if img.mode not in ('RGB',):
                img = img.convert('RGB')

            # Get current dimensions
            width, height = img.size
            
            # Calculate the new size, preserving aspect ratio
            if width > MAX_WIDTH or height > MAX_HEIGHT:
                aspect_ratio = width / height
                if aspect_ratio > 1:
                    # Image is wider than tall (landscape)
                    new_width = min(MAX_WIDTH, width)
                    new_height = int(new_width / aspect_ratio)
                else:
                    # Image is taller than wide (portrait)
                    new_height = min(MAX_HEIGHT, height)
                    new_width = int(new_height * aspect_ratio)
                
                # Resize the image
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
            
            # Save the image with reduced quality
            img.save(target_dir, format='JPEG', quality=QUALITY, optimize=True)
    
    except Exception as e:
        print(f'Error optimizing image {target_dir}: {e}')


def scan_and_optimize_images(target_dir):
    """Scan the directory for image files and optimize them."""
    for root, _, files in os.walk(target_dir):
        for file in files:
            # Check if the file is an image based on the extension
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(root, file)
                optimize_image(image_path)


if __name__ == '__main__':
  
    target_dir = '<target_path>'
    
    # Scan directories and optimize images
    scan_and_optimize_images(target_dir)
