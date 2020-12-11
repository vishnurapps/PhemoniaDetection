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
    device = get_device()

    test_tfms = Compose([Resize((224,224)) , ToTensor()])

    model = PneumoniaModel()
    model.load_state_dict(torch.load("trained_image.data"))
    model.to(device)

    img = Image.open("sample_pneumonia.jpg")
    #img.save("sample.jpg")
    img = test_tfms(img)
    result = model(img.unsqueeze(0)) 
    output = {'data': {'disease':result.item(),'path':'/tmp/sample.jpg'}}
    return json.dumps(output)

if __name__ == "__main__":  
    print(predict_disease("sample"))