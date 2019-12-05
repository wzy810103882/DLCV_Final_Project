import argparse
from PIL import Image


if __name__ == '__main__':
    parser = argparse.ArgumentParser() # get default parameter (config.py)

    # input image and harmonization mask image
    parser.add_argument('--input_dir', help='input image dir', required=True) 
    parser.add_argument('--width', help='training image name',required=True)
    parser.add_argument('--height', help='input reference dir',required=True)
    parser.add_argument('--output_dir', help='reference image name')

    opt = parser.parse_args()

    img = Image.open(opt.input_dir)
    
    img = img.resize((int(opt.width), int(opt.height)))

    if not opt.output_dir:
        img.save(opt.input_dir)
    else:
        img.save(opt.output_dir)    