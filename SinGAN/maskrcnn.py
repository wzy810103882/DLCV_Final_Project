# from MaskRCNN import engine, utils
# from engine import train_one_epoch, evaluate
import torchvision.transforms as T

import os
import numpy as np
import torch
import torch.utils.data
from PIL import Image
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
import argparse

parser = argparse.ArgumentParser(description='Generate Masks.')
parser.add_argument('--img_path',
                   help='the image to be cut')
parser.add_argument('--threshold', default=0.9,
                   help='confidence threshold')
args = parser.parse_args()

img = Image.open(args.img_path).convert("RGB")
img_name = args.img_path.split('/')[-1]
mask_name = img_name.split('.')[0]+'_mask'
img.save('Input/Harmonization/'+img_name)
trans1 = T.ToTensor()
img = trans1(img)


def get_instance_segmentation_model(num_classes):
    # load an instance segmentation model pre-trained on COCO
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

    # get the number of input features for the classifier
    # in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    # model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    # now get the number of input features for the mask classifier
    # in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    # hidden_layer = 256
    # and replace the mask predictor with a new one
    # model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
    #  hidden_layer,
    #  num_classes)

    return model


device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
num_classes = 2
model = get_instance_segmentation_model(num_classes)
model.to(device)
model.eval()
with torch.no_grad():
    prediction = model([img.to(device)])

i = 0
for s in prediction[0]['scores']:
    if s < float(args.threshold):
        break
    i += 1

ary = np.sum(prediction[0]['masks'].mul(255).byte().cpu().numpy()[:i, 0], axis=0)
mask = Image.fromarray(ary.astype('uint8')).convert('RGB')

mask.save('Input/Harmonization/'+mask_name+'.png')
