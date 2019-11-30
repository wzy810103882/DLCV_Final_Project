from skimage.transform import resize
import numpy as np
from skimage import io
import os
from PIL import Image

def img_read(img_path):
    return np.float32(io.imread(img_path)) / 255.0

def img_write(img, img_path):
    io.imsave(img_path, img)

def img_resize(img, height, width):
    return resize(img, (height, width), order = 1)

def main():
    img = img_read("Data/background/background_001.png")   
    height = 500
    width = 500
    resized = img_resize(img,height,width)
    img_write(resized,"Data/background/background_001_small.png")


def insert_human_to_background():
    background = Image.open("SinGAN/Input/Images/background_001_small.png") 
    human = Image.open("Data/Insert/human_001.png") 
    #background.show()
    #human.show()
    human_background_ratio = 0.2
    scale = background.size[0] * human_background_ratio / human.size[0]

    width, height = int(human.size[0] * scale), int(human.size[1] * scale)
    human = human.resize((width, height), Image.ANTIALIAS)
    #human.show()

    bg_width, bg_height = background.size
    x_ratio = 0.7
    y_ratio = 0.7
    x = int(x_ratio * bg_width)
    y = int(y_ratio * bg_height)

    background.paste(human, (x, y), human)
    background.save("SinGAN/Input/Harmonization/human.png")

    #background.show()

    background = Image.new('RGB', (bg_width, bg_height))

    human_width, human_height = human.size
    human_mask = Image.new('RGBA', (human_width,human_height), (0, 0, 0, 0))

    for i in range(human_width):
        for j in range(human_height):
            _,_,_,a = human.getpixel((i,j))
            if a != 0:
                human_mask.putpixel((i,j), (255,255,255,255))

    #human_mask.show()

    background.paste(human_mask, (x, y), human_mask)
    #background.show()
    background.save("SinGAN/Input/Harmonization/human_mask.png")

insert_human_to_background()
    #bg_height, bg_width, _ = background.shape
    #human_height, human_width, _ = resized_human.shape


