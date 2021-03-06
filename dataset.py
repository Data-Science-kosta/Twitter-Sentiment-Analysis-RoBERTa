# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 22:20:41 2021

@author: kosta
"""
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn

class MyDataset(Dataset):
    def __init__(self,df_train):
        self.X_train = df_train['Tweet'].to_list()
        self.Y_train, self.labels = pd.factorize(df_train['HandLabel'],sort=True)
    def __len__(self):
        return len(self.X_train)
    def __getitem__(self,index):
        return self.X_train[index], self.Y_train[index]