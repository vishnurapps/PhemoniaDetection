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
from sklearn.model_selection import train_test_split
from fastprogress.fastprogress import master_bar, progress_bar
from torchvision.transforms.functional import to_grayscale
from sklearn.metrics import accuracy_score, roc_auc_score
from backbone import PneumoniaModel
from resnetdataset import PneumoniaDatset
from resnetutils import set_seed, perf_measure, list_files, get_device, training_step, validation_step, get_data, fit, get_preds

if __name__ == '__main__':
    set_seed(42)
    bs = 8
    device = get_device()
    train_tfms = Compose([ T.RandomAffine(degrees=(-10,10),scale=(0.3, 0.8)),  Resize((224,224)),  ToTensor(), T.RandomErasing(inplace=True)])
    test_tfms = Compose([Grayscale(), Resize((224,224)) , ToTensor()])
    train_data, valid_data = train_test_split(data, test_size=0.2, random_state=42, shuffle=True, stratify=data.Target)
    model = PneumoniaModel()
    model.load_state_dict(torch.load("trained_image.data"))
    model.to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-5,weight_decay=0.01)

    train_ds = PneumoniaDatset(df=train_data,transforms=train_tfms)
    train_dl = DataLoader(dataset=train_ds,batch_size=bs,shuffle=True,num_workers=4)

    train_dl,valid_dl = get_data(train_data,valid_data,train_tfms,test_tfms,bs=64)
    model, val_rocs, train_loss, valid_loss = fit(50,model,train_dl,valid_dl,opt)

    plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(train_loss, '-bx')
    plt.plot(valid_loss, '-rx')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(['Training', 'Validation'])
    plt.title('Loss vs. No. of epochs');
    plt.grid()
    plt.savefig('loss_epoch.png')

    torch.save(model.state_dict(), "trained_image.data")

    preds = get_preds(model, tta=1)
    
    valid_data['prediction'] = preds

    TP, FP, TN, FN = perf_measure(valid_data["Target"], valid_data['prediction'])
    print("Accuracy = ",(TP+TN)/(TP+FP+TN+FN))
    print("Sensitivity = ",(TP)/(TP+FN))                 #When it's actually yes, how often does it predict yes?
    print("Specificity = ",(TN)/(FP+TN))                 #When it's actually no, how often does it predict no?
    print("Misclassification = ",(FP+FN)/(TP+FP+TN+FN))
    cm = confusion_matrix(valid_data['prediction'], valid_data["Target"])
    fig = sns.heatmap(cm, annot=True, fmt="d")
    fig.figure.savefig("confusion_matrix.png")

