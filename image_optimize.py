import os
from PIL import Image
from os import listdir
from os.path import isfile, join

p_from = '\\Users\\sergi\\Documents\\MyProjects\\Web\\Python\\python-wiki\\api\\old\\'
p_to = '\\Users\\sergi\\Documents\\MyProjects\\Web\\Python\\python-wiki\\api\\static\\'


def get_list():
    return [f for f in listdir(p_from) if isfile(join(p_from, f))]


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def get_image(path):
    image = Image.open(path)
    if image.mode in ("RGBA", "P"):
        return image.convert("RGB")
    return image


def crop_image(image, new_width, new_height):
    width, height = image.size

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    return image.crop((left, top, right, bottom))


def resize_image(image, width, height):
    return image.resize((width, height), Image.Resampling.LANCZOS)


def optimize_image(image, path):
    image.save(path, format='JPEG', optimize=True, quality=95)


def calculate_ratio(width, height, max_width, max_height):
    ratio = max(max_width / width, max_height / height)
    return [round(width * ratio), round(height * ratio)]


def calculate_image(image):
    tw, th = [400, 500]
    width, height = image.size
    ratio = width / height
    if ratio == 1:  # square
        x = min(th, width)
        return [x, x]
    else:
        return calculate_ratio(width, height, tw, th)


for item in get_list():
    try:
        image = get_image(f'{p_from}{item}')
        width, height = calculate_image(image)
        image = resize_image(image, width, height)
        optimize_image(image, f'{p_to}{item}')
        delete_file(f'{p_from}{item}')
    except Exception as e:
        print(item, str(e))
