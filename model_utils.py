# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 22:21:26 2021

@author: kosta
"""
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from statistics import mean
import pickle
import os
import numpy as np 
import pandas as pd

def wrap_tokenizer(tokenizer):
    def tokenize(tweet):
        tweet = list(tweet)
        tokens = tokenizer(
            tweet,
            padding=True, 
            return_attention_mask=False,
            truncation=True,
            return_tensors='pt'
            )['input_ids']
        return tokens
    return tokenize

def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']


def train_step(train_loader, tokenize, device, optimizer,scheduler, xlmr, classifier,dropout,logs):
    xlmr.train()
    classifier.train()
    dropout.train()
    iteration = 0
    accuracy = []
    losses = []
    for tweet, target in train_loader:
        logs['lr'].append(get_lr(optimizer))
        target = target.to(device)
        tokens = tokenize(tweet)
        tokens = tokens.to(device)
        embeddings = xlmr.extract_features(tokens)
        first_emb = embeddings[:,0,:]
        first_emb = dropout(first_emb)
        logits = classifier(first_emb)
        loss = nn.CrossEntropyLoss()(input=logits, target=target)
        loss.backward()
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
        # calculate accuracy
        prob = nn.functional.softmax(logits,dim=1)
        prediction = torch.argmax(prob, dim=1)
        acc = torch.sum(target==prediction)/float(len(target))
        accuracy.append(float(acc))
        losses.append(float(loss.detach().cpu().numpy()))
        iteration+=1
        print(f"\r iter: {iteration}/{len(train_loader)}",end='')
    return accuracy, losses
def val_step(val_loader, tokenize, device, xlmr, classifier,dropout, is_test=False):
    print('')
    print('Validating...')
    xlmr.eval()
    classifier.eval()
    dropout.eval()
    iteration = 0
    accuracy, losses = [],[]
    if is_test:
        predictions, targets = [], []
    for tweet, target in val_loader:
        target = target.to(device)
        tokens = tokenize(tweet)
        tokens = tokens.to(device)
        with torch.no_grad():
            embeddings = xlmr.extract_features(tokens)
            first_emb = embeddings[:,0,:]
            first_emb = dropout(first_emb)
            logits = classifier(first_emb)

        loss = nn.CrossEntropyLoss()(input=logits, target=target)
        # calculate accuracy
        prob = nn.functional.softmax(logits,dim=1)
        prediction = torch.argmax(prob, dim=1)
        acc = torch.sum(target==prediction)/float(len(target))
        if is_test:
            predictions.append(prediction.cpu().numpy())
            targets.append(target.cpu().numpy())
        accuracy.append(float(acc))
        losses.append(float(loss.cpu().numpy()))
        iteration+=1
        print(f"\r iter: {iteration}/{len(val_loader)}",end='')
    if is_test:
        return accuracy, losses, predictions, targets
    return accuracy, losses