#coding=utf-8
import csv
import os
import sys
import word2vec
import nltk
import random
import math
import numpy as np
#from emd import emd
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import time
reload(sys)
sys.setdefaultencoding('utf-8') 
global model

remove_list = ['@', '#', "'m", "'re", 'rt', '&', 'http', "'ve", 'wo', "n't", '%']

def load_word2vec_model(filepath = '../../model/GoogleNews-vectors-negative300.bin.gz'):
    global model
#    model = word2vec.load(filepath)
    model = gensim.models.KeyedVectors.load_word2vec_format('../../model/GoogleNews-vectors-negative300.bin', binary=True)

def load_all_data(filepath = 'full-corpus.csv'):
    fr = open(filepath)
    tags = ['neutral', 'positive', 'negative']
    reader = csv.reader(fr)
    i = 0
    label_list = []
    twitter_list = []
    for array in reader:
        if i == 0:
            i += 1
            continue
        if len(array) != 5:
            continue
        if array[1] not in tags:
            continue
        label_list.append(array[1])
        content = array[4]
        content = content.replace('http://t.co/', ' ')
        tokens = tokenize(array[4].decode('utf-8').strip().replace('\n', ' '))
        if len(tokens) == 0:
            continue
        tokenized_content = ' '.join(tokens)
        twitter_list.append(tokenized_content)
        print array[1] + '\t' + tokenized_content
        i += 1
    fr.close()
    return label_list, twitter_list

def tokenize(content):
    raw_tokens = nltk.word_tokenize(content)
    tokens = []
    stop_words = load_stop_words()
    for i in raw_tokens:
        word = i.lower()
        if word in stop_words or word not in model or word in remove_list or word.isdigit():
            continue
        else:
            tokens.append(word)
    return tokens

def load_stop_words(filepath = 'smart_stop_words'):
    stop_words = set()
    fr = open(filepath)
    for line in fr.readlines():
        if line.strip() == '':
            continue
        word = line.strip()
        stop_words.add(word)
    return stop_words

if __name__=='__main__':
    load_word2vec_model()
    label_list, twitter_list = load_all_data()
