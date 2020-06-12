import random
import matplotlib.pyplot as plt
from PIL import Image

I = Image.open('./data/foreground/kh.png')

plt.axis('off')
plt.imshow(I)
plt.show()

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

def transform_image(image, min_width, min_height, max_width, max_height, maintain_ratio=True):
    ''' Applies a random rotation and scale to image '''
    image = image.rotate(random.randint(0, 359), expand=True)
    image = scale_image(image, random.randint(min_width, max_width), random.randint(min_height, max_height), maintain_ratio)
    return image
