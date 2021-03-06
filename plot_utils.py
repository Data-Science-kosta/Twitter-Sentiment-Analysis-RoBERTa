# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 22:16:31 2021

@author: kosta
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import pickle
from statistics import mean
from sklearn.metrics import confusion_matrix
import seaborn as sn

def plot_example_distribution(df_train, df_test, df_val):
    fig = plt.figure(figsize=(18,4))
    titles = ['Train set','Test set','Val set']
    for i,df in enumerate([df_train,df_test,df_val]):
        ax = fig.add_subplot(1,3,i+1)
        Y, labels = pd.factorize(df['HandLabel'],sort=True)
        ax.bar(x=range(3), height=pd.Series(Y).value_counts())
        ax.set_xticks(ticks=range(len(labels)))
        ax.set_xticklabels(labels,fontsize=10)
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Number of examples')
        ax.set_title(titles[i])
    plt.show()
    return
    
def average(data, frequency, start_avg_point=0):
    average_data = []
    if (len(data) > start_avg_point):
        round_num = -(len(str(frequency))-1)
        for i in range(0,round(len(data),round_num)-frequency,frequency):
            avg_data=mean(data[i:i+frequency])
            average_data.append(avg_data)
    return average_data

CMAP = sn.light_palette("blue")
def plot_attentions(att, labs, ax, annot=False, cmap = CMAP, title=None):
    '''
    plot the NxN matrix passed as a heat map

    mat: square matrix to visualize
    labs: labels for xticks and yticks (the tokens in our case)
    '''
    att = att.detach().cpu().numpy()
    ax = sn.heatmap(att, annot=annot, yticklabels=labs,xticklabels=labs, cmap=cmap)
    ax.xaxis.set_ticks_position('top')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=60,fontsize=11)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=11)
    ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
    if title:
        ax.set_title(title,fontsize=14)
    return
