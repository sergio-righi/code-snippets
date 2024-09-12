import os
from PIL import Image
from os import listdir
from os.path import isfile, join
from pathlib import Path
import pillow_avif

target_dir = '<target_path>'

def get_list():
    return [f for f in listdir(target_dir) if isfile(join(target_dir, f))]


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def get_image(path):
    image = Image.open(path).convert("RGB")
    filename = Path(path).stem
    image.save(f'{target_dir}{filename}.jpg', format='jpeg', lossless=True)
    return image


for item in get_list():
    try:
        extension = Path(item).suffix
        if (extension == '.avif'):
            image = get_image(f'{target_dir}{item}')
            delete_file(f'{target_dir}{item}')
    except Exception as e:
        print(item, str(e))
