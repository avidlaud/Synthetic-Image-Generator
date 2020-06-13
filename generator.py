''' Generates synthetic labeled image data '''

import random
import glob
import os
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageDraw

#Draw boxes for debugging
draw_boxes = False

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

def overlay_image(image, background, image_class, file_name):
    ''' Places image on the background '''
    img_width, img_height = image.size
    background_width, background_height = background.size
    width_bound = background_width - img_width
    height_bound = background_height - img_height
    x_coord = random.randint(0, width_bound)
    y_coord = random.randint(0, height_bound)
    background.paste(image, (x_coord, y_coord), image)

    #Draw rectangle for debugging
    if(draw_boxes):
        draw = ImageDraw.Draw(background)
        draw.rectangle(((x_coord, y_coord), (x_coord + img_width, y_coord + img_height)))

    #Get values for writing to file
    x_center = (x_coord + (img_width/2))/background_width
    y_center = (x_coord + (img_height/2))/background_height
    rel_width = img_width / background_width
    rel_height = img_height / background_height
    write_label(image_class, x_center, y_center, rel_width, rel_height, file_name)
    return background

def multi_overlay(images, background, image_classes, file_name):
    ''' Places multiple images on the background without overlap '''
    background_width, background_height = background.size
    excluded_x = []
    excluded_y = []
    ###
    #
    #   USE TUPLES INSTEAD OF THIS
    #
    ###
    #excluded_range = []
    for i, image in enumerate(images):
        img_width, img_height = image.size
        width_bound = background_width - img_width
        height_bound = background_height - img_height
        if len(excluded_x) != 0:
            allowed_width = [x for x in list(range(0, width_bound)) if x not in excluded_x and x+img_width not in excluded_x]
            allowed_height = [y for y in list(range(0, height_bound)) if y not in excluded_y and y+img_height not in excluded_y]
            print(excluded_x)
            x_coord = random.choice(allowed_width)
            y_coord = random.choice(allowed_height)
            print("IF")
        else:
            x_coord = random.randint(0, width_bound)
            y_coord = random.randint(0, height_bound)
            print("ELSE")
        excluded_x += list(range(x_coord, x_coord + img_width))
        excluded_y += list(range(y_coord, y_coord + img_height))
        background.paste(image, (x_coord, y_coord), image)
        
        #Get values for writing to file
        x_center = (x_coord + (img_width/2))/background_width
        y_center = (x_coord + (img_height/2))/background_height
        rel_width = img_width / background_width
        rel_height = img_height / background_height
        image_class = image_classes[i]
        write_label(image_class, x_center, y_center, rel_width, rel_height, file_name)
    return background

def write_label(image_class, x_center, y_center, width, height, file_name):
    ''' Create a corresponding label text file '''
    file_path = file_name + ".txt"
    label_file = open(file_path, "a+")
    x_c = '%.6f'%(x_center)
    y_c = '%.6f'%(y_center)
    w = '%.6f'%(width)
    h = '%.6f'%(height)
    label_file.write(str(image_class) + " " + x_c + " " + y_c + " " + w + " " + h + "\n")
    label_file.close()

def main():
    #Path to folder of images
    IMAGES_PATH = 'data/foreground/*.png'
    #Path to folder of backgrounds
    BACKGROUNDS_PATH = 'data/background/*.jpg'
    #Path to output
    OUTPUT_IMAGE_PATH = 'output/images/'
    #Path to label folder
    OUTPUT_LABEL_PATH = 'output/labels/'
    #Number of images to generate per image per background
    NUM_IMAGES = 0
    #Number of 2-image outputs
    NUM_TWO_IMAGES = 5000
    #Randomly pick backgrounds
    RANDOM_BACKGROUND = False
    #Keep aspect ratio for transformed images
    MAINTAIN_ASPECT_RATIO = True
    
    MIN_IMAGE_WIDTH = 150
    MAX_IMAGE_WIDTH = 250
    MIN_IMAGE_HEIGHT = 150
    MAX_IMAGE_HEIGHT = 250

    MIN_TWO_IMAGE_WIDTH = 75
    MAX_TWO_IMAGE_WIDTH = 125
    MIN_TWO_IMAGE_HEIGHT = 75
    MAX_TWO_IMAGE_HEIGHT = 125

    BACKGROUND_WIDTH = 512
    BACKGROUND_HEIGHT = 512

    images = glob.glob(IMAGES_PATH)
    backgrounds = glob.glob(BACKGROUNDS_PATH)

    image_counter = 0

    #Single image per output
    for image_path in images:
        image_class = os.path.splitext(os.path.basename(image_path))[0]
        original_image = Image.open(image_path)
        for background_path in backgrounds:
            for i in range(NUM_IMAGES):
                background = Image.open(background_path)
                background = scale_image(background, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
                image_width = random.randint(MIN_IMAGE_WIDTH, MAX_IMAGE_WIDTH)
                image_height = random.randint(MIN_IMAGE_HEIGHT, MAX_IMAGE_HEIGHT)
                image = scale_image(rotate_image(original_image), image_width, image_height)
                file_name = "output_" + '%06d'%(image_counter)
                overlayed = overlay_image(image, background, image_class, OUTPUT_LABEL_PATH + file_name)
                overlayed.save(OUTPUT_IMAGE_PATH + file_name + ".jpg")
                image_counter += 1
                plt.imshow(overlayed)
                plt.show()
    
    #Two images per output
    for j in range(NUM_TWO_IMAGES):
        choice1 = random.choice(images)
        choice2 = random.choice(images)
        image_class1 = os.path.splitext(os.path.basename(choice1))[0]
        image_class2 = os.path.splitext(os.path.basename(choice2))[0]
        original_image1 = Image.open(choice1)
        original_image2 = Image.open(choice2)
        background = Image.open(random.choice(backgrounds))
        background = scale_image(background, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        image_width = random.randint(MIN_TWO_IMAGE_WIDTH, MAX_TWO_IMAGE_WIDTH)
        image_height = random.randint(MIN_TWO_IMAGE_HEIGHT, MAX_TWO_IMAGE_HEIGHT)
        image1 = scale_image(rotate_image(original_image1), image_width, image_height)
        image2 = scale_image(rotate_image(original_image2), image_width, image_height)
        file_name = "output_" + '%06d'%(image_counter)
        overlayed = multi_overlay([image1, image2], background, [image_class1, image_class2], OUTPUT_LABEL_PATH + file_name)
        overlayed.save(OUTPUT_IMAGE_PATH + file_name + ".jpg")
        image_counter += 1
        plt.imshow(overlayed)
        plt.show()

if __name__ == "__main__": main()
