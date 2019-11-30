from skimage.transform import resize
import numpy as np
from skimage import io


def img_read(img_path):
    return np.float32(io.imread(img_path))/255.0

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
