''' Generates synthetic labeled image data '''

import random
import glob
import matplotlib.pyplot as plt
from PIL import Image

def scale_image(image, width, height, maintain_ratio=True):
    ''' Resizes an image to a given size, can maintain aspect ratio '''
    w, h = image.size
    if not maintain_ratio:
        image = image.resize((width, height), Image.LANCZOS)
    else:
        #Scale by the "longer" side
        scale_factor = width / w if w/h > width/height else height / h
        image = image.resize((round(w*scale_factor), round(h*scale_factor)), Image.LANCZOS)
    return image

def rotate_image(image):
    ''' Applies a random rotation to the image '''
    return image.rotate(random.randint(0, 359), expand=True)

def overlay_image(image, background):
    ''' Places image on the background '''
    img_width, img_height = image.size
    background_width, background_height = background.size
    width_bound = background_width - img_width
    height_bound = background_height - img_height
    background.paste(image, (random.randint(0, width_bound), random.randint(0, height_bound)), image)
    return background

def main():
    #Path to folder of images
    IMAGES_PATH = ''
    #Path to folder of backgrounds
    BACKGROUNDS_PATH = ''
    #Path to output
    OUTPUT_PATH = ''

    images = glob.glob(IMAGES_PATH)
    backgrounds = glob.glob(BACKGROUNDS_PATH)


if __name__ == "__main__": main()