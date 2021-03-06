# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 22:07:24 2021

@author: kosta
"""
import regex as re
import os
import pandas as pd
import numpy as np
import sys

def preprocess_dataset1(df):
    n_rows = len(df)
    df = df.dropna()
    # if you have duplicate tweets with same hand label keep one
    print(f'Dropped {n_rows - len(df)} NaN rows')
    n_rows = len(df)
    df = df.drop_duplicates(subset=['Tweet','HandLabel'], keep='first')
    print(f'Dropped {n_rows - len(df)} duplicate rows with same HandLabel')
    # now there are only duplicates with different hand label, so drop both of them
    n_rows = len(df)
    df = df.drop_duplicates(subset=['Tweet'],keep=False)
    print(f'Dropped {n_rows - len(df)} duplicate rows with different HandLabel')
    df = df.drop(columns=['Unnamed: 0'])
    df = preprocess_tweets(df)
    print(f'Final number of rows: {len(df)}')
    return df

def preprocess_dataset2(df):
    df.rename(columns={'text':'Tweet'},inplace=True)
    n_rows = len(df)
    df = preprocess_tweets(df)
    return df

def preprocess_tweets(df):
    # convert to lower case
    df['Tweet'] = df.Tweet.str.lower()
    # remove links
    df.Tweet = df.Tweet.apply(lambda x: re.sub(r'https?:\/\/\S+', '', x))
    df.Tweet = df.Tweet.apply(lambda x: re.sub(r"www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', x))
    df.Tweet = df.Tweet.apply(lambda x: re.sub(r'{link}', '', x))
    df.Tweet = df.Tweet.apply(lambda x: re.sub(r"\[video\]", '', x))
    # substitute 'RT @' with '@'
    df.Tweet = df.Tweet.apply(lambda x: re.compile('rt @').sub('@', x).strip())
    # Remove usernames. The usernames are any word that starts with @.
    df.Tweet = df.Tweet.apply(lambda x: re.sub('\@[a-zA-Z0-9]*', '', x))
    # convert '#' to '' and '_' to ' ' and ':' to ''
    df.Tweet = df.Tweet.apply(lambda x: x.replace("#", "").replace("_", " ").replace(":",""))
    return df

def schuffle_df(df):
    ind = np.random.permutation(len(df))
    df = df.iloc[ind,:]
    return df