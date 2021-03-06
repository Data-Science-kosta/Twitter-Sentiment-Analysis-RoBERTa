# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 22:09:31 2021

@author: kosta
"""
import os
import tweepy
import pandas as pd
import numpy as np
import sys

def get_keys(path):
    with open(path,'r') as f:
        lines = f.readlines()
    keys = []
    for i, line in enumerate(lines):
        lines[i] = line.strip('\n').strip(':')
    for i,line in enumerate(lines):
        if line=='API key':
            CONSUMER_KEY = lines[i+1]
        if line=='API secret key':
            CONSUMER_SECRET = lines[i+1]
        if line=='Access token':
            OAUTH_TOKEN = lines[i+1]
        if line=='Access token secret':
            OAUTH_TOKEN_SECRET = lines[i+1]   
    return CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def connect_to_API(path_keys):
    CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET = get_keys(path_keys)
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)
    print('Connected Successfuly!')
    return api

def get_tweet(api, tweet_id):
    tweet = api.get_status(id=tweet_id, tweet_mode='extended')
    return tweet.full_text

def extract_tweets(api,lg, data_path, start_row=0):
    path_ids = os.path.join(data_path, 'ids_only')
    path_tweets = os.path.join(data_path, 'with_tweets')
    os.makedirs(path_tweets, exist_ok=True)
    path_tweets = os.path.join(path_tweets, lg)
    os.makedirs(path_tweets, exist_ok=True)
    file_path = os.path.join(path_ids,lg+'_Twitter_sentiment.csv')
    df = pd.read_csv(file_path)
    df_out = pd.DataFrame(columns=list(df.columns)+['Tweet'])
    n_rows = len(df)
    for i in range(start_row,n_rows):
        print(f'\rTweet ID: {i}/{n_rows}',end='')
        tweet_id = df.loc[i,'TweetID']
        try:
            tweet = get_tweet(api,str(tweet_id))
        except tweepy.TweepError:
            tweet = None
        df_out = df_out.append({
            'TweetID':tweet_id,
            'HandLabel':df.loc[i,'HandLabel'],
            'AnnotatorID':df.loc[i,'AnnotatorID'],
            'Tweet':tweet
            }, 
            ignore_index=True
        )
        del tweet
        del tweet_id
        if i % 5000 == 0 and i != 0:
            df_out.to_csv(os.path.join(path_tweets,lg+f'_Twitter_sentiment_s_{start_row}_e_{i}.csv'))
    df_out.to_csv(os.path.join(path_tweets,lg+f'_Twitter_sentiment_s_{start_row}_e_{n_rows-1}.csv'))
    