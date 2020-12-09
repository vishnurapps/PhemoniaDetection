import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F

class PneumoniaModel(nn.Module):
    def __init__(self, backbone=models.resnet34(pretrained=True), n_out=1):
        super().__init__()
        backbone = backbone
        in_features = backbone.fc.in_features
        backbone.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.backbone = nn.Sequential(*list(backbone.children())[:-2])
        self.classifier = nn.Sequential(nn.Linear(in_features, n_out))
        
    def forward(self, x):
        x = self.backbone(x)              
        x = F.adaptive_avg_pool2d(x, 1)  
        x = torch.flatten(x, 1)           
        x = self.classifier(x)            
        return x