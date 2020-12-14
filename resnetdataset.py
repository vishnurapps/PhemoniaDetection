import os
import random
import pandas as pd
import numpy as np
import cv2 as cv
import pydicom
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
import torch
from pathlib import Path
from torch.utils.data import Dataset,DataLoader
from PIL import Image
from torchvision import transforms as T
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import Resize, Compose, ToTensor, Grayscale
import torchvision.models as models
from fastprogress.fastprogress import master_bar, progress_bar
from torchvision.transforms.functional import to_grayscale
from sklearn.metrics import accuracy_score, roc_auc_score

class PneumoniaDatset(Dataset):
    def __init__(self, df, transforms=None, is_test=False):
        self.df = df
        self.transforms = transforms
        self.is_test = is_test
    
    def __getitem__(self, idx):
        image_path = f"./input/images/{self.df.iloc[idx]['patientId']}.jpg"
        img = Image.open(image_path)
        
        if self.transforms:
            img = self.transforms(img)
        if self.is_test:
            return img
        else:
            disease = self.df.iloc[idx]['Target']
            return img, torch.tensor([disease], dtype=torch.float32)
        
    def __len__(self):
        return self.df.shape[0]