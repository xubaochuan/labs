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

remove_list = ['@', '#', "'m", "'re", '&', "'ve", 'wo', "n't", '%', "'ll"]

def load_word2vec_model(filepath = '../../model/GoogleNews-vectors-negative300.bin.gz'):
    global model
    model = gensim.models.KeyedVectors.load_word2vec_format(filepath, binary=True)

def load_all_data(filepath = 'bbcsports.txt'):
    fr = open(filepath)
    label_list = []
    twitter_list = []
    for line in fr.readlines():
        array = line.strip().split('\t')
        if '\t' not in line or len(array) != 2:
            continue
        label_list.append(array[0])
        content = array[1].strip().decode('utf-8')
        tokens = tokenize(content)
        if len(tokens) == 0:
            continue
        tokenized_content = ' '.join(tokens)
        twitter_list.append(tokenized_content)
        print array[0] + '\t' + tokenized_content
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

def load_stop_words(filepath = 'smart_stop_words_full.txt'):
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
