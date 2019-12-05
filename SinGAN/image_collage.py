import sys
from PIL import Image, ImageFont, ImageDraw
import argparse
import math
import glob 
import os
def generate_with_caption(img,caption):
    width,height = img.size
    result = Image.new('RGBA',(width+10, int(1.25 *height)), 'white')
    result.paste(img,(5,5,width+5,height+5))
    #font = ImageFont.truetype("arial.ttf", 100)

    img_fraction = 0.15
    fontsize = 1
    font = ImageFont.truetype("arial.ttf", fontsize)
    while font.getsize(caption)[1] < img_fraction*img.size[1]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("arial.ttf", fontsize)

    w,h = font.getsize(caption)
    draw = ImageDraw.Draw(result)
    draw.text(  ((width-w) // 2  , int(1.07 * height)) , caption, font=font, fill = "black" )
    return result
    #result.show()

if __name__ == "__main__":
    #img = Image.open("/Users/ouchouyang/Desktop/basketball.png")
    #caption = "basketball"
    #generate_with_caption(img,caption)
    
    parser = argparse.ArgumentParser() # get default parameter (config.py)

    # input image and harmonization mask image
    parser.add_argument('--train_img', help='train image dir', required=True) 
    parser.add_argument('--test_img', help='test image dir', required=True) 

    parser.add_argument('--result_dir', help='test image dir', required=True) 

    parser.add_argument('--output_dir', help='output image dir',default = 'Output/Collage')

    opt = parser.parse_args()

    result_dir = opt.result_dir 
    result_img_names = sorted(glob.glob(result_dir + "/" + '*.png'),key=lambda name: int(os.path.basename(name)[12:-4]))

    result_imgs = [Image.open(x) for x in result_img_names]

    train_img = Image.open(opt.train_img) 
    test_img = Image.open(opt.test_img)

    #widths, heights = zip(*(i.size for i in images))
    #new_width  = 680
    #new_height = new_width * height / width 
    print(result_imgs[0].size)
    train_img = train_img.resize(result_imgs[0].size, Image.ANTIALIAS)
    test_img = test_img.resize(result_imgs[0].size, Image.ANTIALIAS)

    #print(result_img_names[0][:-4])
    #print(os.path.basename(your_path))

    result_imgs = [generate_with_caption(x,os.path.basename(result_img_names[i])[:-4]) for i,x in enumerate(result_imgs)]
    
    train_img = generate_with_caption(train_img,"Training")
    test_img = generate_with_caption(test_img,"Input")

    total_width = (math.ceil(len(result_imgs) / 2) + 1)* result_imgs[0].size[0]
    max_height = result_imgs[0].size[1] * 2
    print(total_width)
    print(max_height)
    #total_width = sum(widths)
    #max_height = max(heights)
    print(len(result_imgs))
    result = Image.new('RGB', (total_width, max_height), 'white')

    width,height = result_imgs[0].size
    
    #width,height = result_imgs.size
    result.paste(test_img, (0,0))
    result.paste(train_img, (0,height))

    x_offset = width
    for i in range(math.ceil(len(result_imgs) / 2)): # some logic issue here, might have two extra spac
        result.paste(result_imgs[i],(x_offset ,0))
        x_offset += width
        print(i)
    print("done")    
    x_offset = width    
    for i in range(math.ceil(len(result_imgs) / 2), len(result_imgs)):
        result.paste(result_imgs[i],(x_offset ,height))    
        x_offset += width 
        print(i)

    result.show()

    counter = 1
    sav_loc = opt.output_dir + "/" + "collage{}.png"
    while os.path.isfile(sav_loc.format(counter)):
        counter += 1
    sav_loc = sav_loc.format(counter)

    result.save(sav_loc)

    #for im in images:
    #new_im.paste(im, (x_offset,0))
    #x_offset += im.size[0]

    #new_im.save('test.jpg')
    