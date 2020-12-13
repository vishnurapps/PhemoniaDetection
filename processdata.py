import random
import pydicom
import torch
from PIL import Image
from torchvision import transforms as T
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import Resize, Compose, ToTensor, Grayscale
import json
from backbone import PneumoniaModel
import pandas as pd
import numpy as np
import cv2
import os
import re
import albumentations as A
import torch
import torchvision

from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.sampler import SequentialSampler
from PIL import Image
from albumentations.pytorch.transforms import ToTensorV2
from matplotlib import pyplot as plt
from tqdm import tqdm
import pydicom as dicom


device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# DIR_INPUT = '../input/rsna-pneumonia-detection-2018/input'
# DIR_TEST = f"{DIR_INPUT}/images"
# test_images = os.listdir(DIR_TEST)
# print(f"Validation instances: {len(test_images)}")

# load a model; pre-trained on COCO
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True, min_size=1024)
num_classes = 2  # 1 class (pnueomonia) + background
# get the number of input features for the classifier
in_features = model.roi_heads.box_predictor.cls_score.in_features
# replace the pre-trained head with a new one
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

os.makedirs('../validation_predictions', exist_ok=True)
model.load_state_dict(torch.load('fasterrcnn_resnet50_fpn.pth' ,map_location=torch.device('cpu')))
model.to(device)

detection_threshold = 0.9
img_num = 0
results = []
model.eval()

def format_prediction_string(boxes, scores):
    pred_strings = []
    for j in zip(scores, boxes):
        pred_strings.append("{0:.4f} {1} {2} {3} {4}".format(j[0], 
                                                             int(j[1][0]), int(j[1][1]), 
                                                             int(j[1][2]), int(j[1][3])))

    return " ".join(pred_strings)

def get_device():
    """
    This is used to get the device to run the training
    """
    return torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def get_image():
    """
    Return image from dicom
    """
    return 

def predict_disease(img_path):
    # device = get_device()

    # test_tfms = Compose([Resize((224,224)) , ToTensor()])

    # model = PneumoniaModel()
    # model.load_state_dict(torch.load("trained_image.data"))
    # model.to(device)

    # img = Image.open("sample_pneumonia.jpg")
    # #img.save("sample.jpg")
    # img = test_tfms(img)
    # result = model(img.unsqueeze(0)) 
    # output = {'data': {'disease':result.item(),'path':'/tmp/sample.jpg'}}
    # return json.dumps(output)

    with torch.no_grad():
        ds = dicom.dcmread(img_path)
        pixel_array_numpy = ds.pixel_array
        image = cv2.cvtColor(pixel_array_numpy, cv2.COLOR_BGR2RGB).astype(np.float32)
        image /= 255.0
        image = np.transpose(image, (2, 0, 1)).astype(np.float)
        image = torch.tensor(image, dtype=torch.float).cpu()
        image = torch.unsqueeze(image, 0)

        model.eval()
        cpu_device = torch.device("cpu")

        outputs = model(image)
        print(outputs)
        outputs = [{k: v.to(cpu_device) for k, v in t.items()} for t in outputs]
        if len(outputs[0]['boxes']) != 0:
            for counter in range(len(outputs[0]['boxes'])):
                boxes = outputs[0]['boxes'].data.cpu().numpy()
                scores = outputs[0]['scores'].data.cpu().numpy()
                boxes = boxes[scores >= detection_threshold].astype(np.int32)
                draw_boxes = boxes.copy()
                boxes[:, 2] = boxes[:, 2] - boxes[:, 0]
                boxes[:, 3] = boxes[:, 3] - boxes[:, 1]
                
            for box in draw_boxes:
                cv2.rectangle(pixel_array_numpy,
                            (int(box[0]), int(box[1])),
                            (int(box[2]), int(box[3])),
                            (0, 10, 0), 3)
        
            plt.imshow(cv2.cvtColor(pixel_array_numpy, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            test_images = img_path.split("/")[-1]
            test_images = test_images.replace('.dcm', '.jpg')
            plt.savefig(f"images/{test_images}")
            plt.close()
                
            result = {
                'patientId': test_images.split('.')[0],
                'PredictionString': format_prediction_string(boxes, scores)
            }
            results.append(result)
        else:
            result = {
                'patientId': test_images.split('.')[0],
                'PredictionString': None
            }
        fr = outputs[0]['scores'].data.cpu().numpy()
        print(np.amax(fr))
        prediction = "suspect" if np.amax(fr) > detection_threshold  else "healthy"
    output = {'data': {'disease':prediction,'path':f"images/{test_images}"}}
    return json.dumps(output)


if __name__ == "__main__":  
    print(predict_disease("sample"))


