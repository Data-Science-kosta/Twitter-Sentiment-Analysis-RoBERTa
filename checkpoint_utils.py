# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 22:25:07 2021

@author: kosta
"""
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from statistics import mean
import pickle
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def save_to_disk(txt_path, values):
    if os.path.isfile(txt_path):
        os.remove(txt_path)
    with open(txt_path, "wb") as fp:   
        pickle.dump(values, fp)
    return
def load_from_disk(txt_path):
    with open(txt_path, "rb") as f:
        values =  pickle.load(f)
    return values

def save_checkpoint_dataset1(xlmr, classifier, optimizer, logs, checkpoint_dir, epoch):
    print('')
    print('Saving checkpoint...')
    state_dict = {
        'classifier':classifier.state_dict(),
        'optimizer': optimizer.state_dict(),
        'xlmr': xlmr.state_dict()
    }
    torch.save(state_dict, os.path.join(checkpoint_dir, 'checkpoint_{}.pt'.format(epoch)))
    save_to_disk(os.path.join(checkpoint_dir, 'logs.txt'),logs)
    print(f'Checkpoint saved!')

def save_checkpoint_dataset2(xlmr, classifier, optimizer, logs, checkpoint_dir, epoch):
    print('')
    print('Saving checkpoint...')
    state_dict = {
        'classifier':classifier.state_dict(),
        'optimizer': optimizer.state_dict(),
        'xlmr': xlmr.state_dict()
    }
    torch.save(state_dict, os.path.join(checkpoint_dir, 'checkpoint_{}.pt'.format(epoch)))
    save_to_disk(os.path.join(checkpoint_dir, 'logs.txt'),logs)
    print(f'Checkpoint saved!')

def load_checkpoint_dataset2(checkpoint_dir, epoch, xlmr, classifier, device, optimizer=None):
    pretrained_dict = torch.load(
        os.path.join(checkpoint_dir,'checkpoint_{}.pt'.format(epoch)),
        map_location=torch.device(device)
        )
    classifier.load_state_dict(pretrained_dict['classifier'])
    try:
        xlmr.load_state_dict(pretrained_dict['xlmr'])
    except RuntimeError:
        print('Initial loading failed. Trying with changed keys!')
        existing_keys = [ 
                        "model.encoder.sentence_encoder.layernorm_embedding.weight",
                        "model.encoder.sentence_encoder.layernorm_embedding.bias"
                        ]
        missing_keys = [
                         "model.encoder.sentence_encoder.emb_layer_norm.weight",
                         "model.encoder.sentence_encoder.emb_layer_norm.bias"
                         ]
        for missing_key, existing_key in zip(missing_keys, existing_keys):
            pretrained_dict['xlmr'][missing_key] = pretrained_dict['xlmr'][existing_key]
            del pretrained_dict['xlmr'][existing_key]
        del pretrained_dict['xlmr']["model.encoder.sentence_encoder.version"]
        xlmr.load_state_dict(pretrained_dict['xlmr'])
    if optimizer is not None:
        optimizer.load_state_dict(pretrained_dict['optimizer'])
    print('Weights are loaded successfuly!')
    return xlmr, classifier, optimizer

class SaveOutput:
    def __init__(self):
        self.outputs = []

    def __call__(self, module, module_in, module_out):
        self.outputs.append(module_out)

    def clear(self):
        self.outputs = []