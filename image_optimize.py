import os
from PIL import Image
from os import listdir
from os.path import isfile, join

# Directory containing original images
INPUT_DIR = ''

# Directory where processed images will be saved
OUTPUT_DIR = ''


def list_input_files():
    """
    Returns a list of file names in the input directory.
    Only includes files (ignores subdirectories).
    """
    return [
        filename
        for filename in listdir(INPUT_DIR)
        if isfile(join(INPUT_DIR, filename))
    ]


def delete_file(file_path):
    """
    Deletes a file at the given path if it exists.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def load_image(file_path):
    """
    Opens an image from disk.
    Converts images with alpha or palette modes to RGB
    so they can be safely saved as JPEG.
    """
    image = Image.open(file_path)
    if image.mode in ("RGBA", "P"):
        return image.convert("RGB")
    return image


def crop_center(image, crop_width, crop_height):
    """
    Crops the image from the center to the specified dimensions.
    """
    image_width, image_height = image.size

    left = (image_width - crop_width) / 2
    top = (image_height - crop_height) / 2
    right = (image_width + crop_width) / 2
    bottom = (image_height + crop_height) / 2

    return image.crop((left, top, right, bottom))


def resize_image(image, target_width, target_height):
    """
    Resizes the image using high-quality Lanczos resampling.
    """
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)


def save_optimized_jpeg(image, output_path):
    """
    Saves the image as an optimized JPEG with high quality.
    """
    image.save(output_path, format='JPEG', optimize=True, quality=95)


def scale_to_fit(original_width, original_height, min_width, min_height):
    """
    Scales dimensions proportionally so the image meets or exceeds
    the target size while preserving aspect ratio.
    """
    scale_ratio = max(min_width / original_width, min_height / original_height)
    return [round(original_width * scale_ratio), round(original_height * scale_ratio)]


def calculate_target_size(image):
    """
    Determines the final dimensions for the image.
    """
    target_width, target_height = 400, 500
    original_width, original_height = image.size

    if original_width / original_height == 1:
        size = min(target_height, original_width)
        return [size, size]

    return scale_to_fit(original_width, original_height, target_width, target_height)


for filename in list_input_files():
    print(filename)
    try:
        image = load_image(join(INPUT_DIR, filename))
        new_width, new_height = calculate_target_size(image)
        resized_image = resize_image(image, new_width, new_height)
        save_optimized_jpeg(resized_image, join(OUTPUT_DIR, filename))
        # delete_file(join(INPUT_DIR, filename))
    except Exception as error:
        print(filename, str(error))
