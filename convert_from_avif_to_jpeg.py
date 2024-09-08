import os
from PIL import Image
from os import listdir
from os.path import isfile, join
from pathlib import Path
import pillow_avif

input_folder = ''

def get_list():
    return [f for f in listdir(input_folder) if isfile(join(input_folder, f))]


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def get_image(path):
    image = Image.open(path).convert("RGB")
    filename = Path(path).stem
    image.save(f'{input_folder}{filename}.jpg', format="jpeg", lossless=True)
    return image


for item in get_list():
    print(f'{item}')
    try:
        extension = Path(item).suffix
        if (extension == '.avif'):
            image = get_image(f'{input_folder}{item}')
            delete_file(f'{input_folder}{item}')
    except Exception as e:
        print(item, str(e))
