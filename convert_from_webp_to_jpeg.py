import os
from PIL import Image
from os import listdir
from os.path import isfile, join
from pathlib import Path

target_folder = ''

def get_list():
    return [f for f in listdir(target_folder) if isfile(join(target_folder, f))]


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def get_image(path):
    image = Image.open(path).convert("RGB")
    filename = Path(path).stem
    image.save(f'{target_folder}{filename}.jpg', format="jpeg", lossless=True)
    return image


for item in get_list():
    print(f'{item}')
    try:
        extension = Path(item).suffix
        if (extension == '.webp'):
            image = get_image(f'{target_folder}{item}')
            delete_file(f'{target_folder}{item}')
    except Exception as e:
        print(item, str(e))
