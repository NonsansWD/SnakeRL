import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy

class BaseNet(nn.Module):
    def __init__(self):
        super(BaseNet, self).__init__()
        self.fc1 = nn.Linear(6, 16, dtype=torch.float64)
        self.fc2 = nn.Linear(16, 32, dtype=torch.float64)
        self.fc3 = nn.Linear(32, 64, dtype=torch.float64)
        self.fc4 = nn.Linear(64, 32, dtype=torch.float64)
        self.fc5 = nn.Linear(32, 16, dtype=torch.float64)
        self.fc6 = nn.Linear(16, 8, dtype=torch.float64)
        self.fc7 = nn.Linear(8, 1, dtype=torch.float64)
    
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = F.relu(x)
        x = self.fc4(x)
        x = F.relu(x)
        x = self.fc5(x)
        x = F.relu(x)
        x = self.fc6(x)
        x = F.relu(x)
        x = self.fc7(x)
        return x
    