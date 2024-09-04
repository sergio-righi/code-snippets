import os
from PIL import Image
from os import listdir
from os.path import isfile, join
from pathlib import Path

p_from = '\\Users\\sergi\\Documents\\MyProjects\\Web\\Python\\python-wiki\\api\\old\\'
p_to = '\\Users\\sergi\\Documents\\MyProjects\\Web\\Python\\python-wiki\\api\\old\\'


def get_list():
    return [f for f in listdir(p_from) if isfile(join(p_from, f))]


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def get_image(path):
    image = Image.open(path).convert("RGB")
    filename = Path(path).stem
    image.save(f'{p_from}{filename}.jpg', format="jpeg", lossless=True)
    return image


for item in get_list():
    print(f'{item}')
    try:
        extension = Path(item).suffix
        if (extension == '.webp'):
            image = get_image(f'{p_from}{item}')
            delete_file(f'{p_from}{item}')
    except Exception as e:
        print(item, str(e))
