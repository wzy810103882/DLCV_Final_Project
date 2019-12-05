import torchvision.transforms as T
import numpy as np
import torch
import torch.utils.data
from PIL import Image
import torchvision

# import argparse
#
# parser = argparse.ArgumentParser(description='Generate Masks.')
# parser.add_argument('--img_path',
#                    help='the image to be cut')
# parser.add_argument('--threshold', default=0.9,
#                    help='confidence threshold')
# args = parser.parse_args()


def get_instance_segmentation_model():
    # load an instance segmentation model pre-trained on COCO
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

    return model


def maskrcnn(img_path): # input an image path, return a cropped rgba image
    # img1 = Image.open(args.img_path).convert("RGB")
    img1 = Image.open(img_path).convert("RGB")
    # img_name = args.img_path.split('/')[-1]
    # mask_name = img_name.split('.')[0]+'_mask'
    # img1.save('Input/Harmonization/'+img_name)
    trans1 = T.ToTensor()
    img = trans1(img1)
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    model = get_instance_segmentation_model()
    model.to(device)
    model.eval()
    with torch.no_grad():
        prediction = model([img.to(device)])

    i = 0
    x1 = len(img[0])
    x2 = 0
    y1 = len(img)
    y2 = 0
    while prediction[0]['scores'][i] >= float(0.9):
        x1_t, y1_t, x2_t, y2_t = prediction[0]['boxes'][i]
        if x1_t < x1:
            x1 = x1_t
        if x2_t > x2:
            x2 = x2_t
        if y1_t < y1:
            y1 = y1_t
        if y2_t > y2:
            y2 = y2_t
        i += 1

    ary = np.sum(prediction[0]['masks'].mul(255).byte().cpu().numpy()[:i, 0], axis=0)
    mask = Image.fromarray(ary.astype('uint8')).convert('RGB')
    mask.crop(box=(int(x1), int(y1), int(x2), int(y2)))

    img1.crop(box=(int(x1), int(y1), int(x2), int(y2)))
    mask = np.asarray(mask)
    width = len(mask[0])
    height = len(mask)

    img_crop = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    for i in range(width):
        for j in range(height):
            r, g, b = img1.getpixel((i, j))
            img_crop.putpixel((i, j), (r, g, b, mask[j][i][0]))

    return img_crop
# mask.save('Input/Harmonization/'+mask_name+'.png')
