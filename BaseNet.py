import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy

class BaseNet(nn.module):
    def __init__(self):
        super(BaseNet, self).__init__()
        self.fc1 = nn.Linear(6, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, 1)
    
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = F.relu(x)
        x = self.fc4(x)
        return x
    