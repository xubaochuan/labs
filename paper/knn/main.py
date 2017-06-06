#coding=utf-8
import csv
import os
import sys
import word2vec
import nltk
import random
import math
import numpy as np
from emd import emd
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import time
reload(sys)
sys.setdefaultencoding('utf-8') 
global model

def load_word2vec_model(filepath = '../model/GoogleNews-vectors-negative300.bin.gz'):
    global model
#    model = word2vec.load(filepath)
    model = gensim.models.KeyedVectors.load_word2vec_format('../model/GoogleNews-vectors-negative300.bin', binary=True)

def load_all_data(filepath = '../data/twitter/full-corpus.csv'):
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
        tokenized_content = tokenize(array[4].decode('utf-8').strip().replace('\n', ' '))
        twitter_list.append(tokenized_content)
        i += 1
    fr.close()
    return label_list, twitter_list

def tokenize(content):
    tokens = nltk.word_tokenize(content)
    return ' '.join(tokens)

def cal_idf(content_list):
    count_dict = {}
    idf_dict = {}
    total = 0.0
    for one in content_list:
        word_list = one.strip().split(' ')
        temp_set = set()
        total += 1
        for word in word_list:
            if word not in temp_set:
                temp_set.add(word)
            else:
                continue
            if word not in count_dict:
                count_dict[word] = 0.0
            count_dict[word] += 1
    for k,v in count_dict.items():
        idf = math.log(total/v)
        idf_dict[k] = idf
    return idf_dict

def load_twitter_vec(twitter_list, idf_dict):
    global model
    word_weight_list = []
    word_vec_list = []
    for one in twitter_list:
        word_count_dict = {}
        sentence_word_weight_list = []
        sentence_word_vec_list = []
        total_word = 0.0
        word_list = one.strip().split(' ')
        for word in word_list:
            if word in model:
                vec = model[word]
            else:
                continue
            if word not in word_count_dict:
                word_count_dict[word] = {}
                word_count_dict[word]['count'] = 0.0
            word_count_dict[word]['count'] += 1
            word_count_dict[word]['vec'] = vec
            total_word += 1
        for k,v in word_count_dict.items():
            idf = idf_dict[k]
#            weight = word_count_dict[k]['count']/total_word*float(idf)
            weight = word_count_dict[k]['count']/total_word
            sentence_word_weight_list.append(weight)
            sentence_word_vec_list.append(word_count_dict[k]['vec'])
        weight_sum = 0.0
        for i in sentence_word_weight_list:
            weight_sum += i
        normalize_word_weight_list = []
        for i in sentence_word_weight_list:
            normalize_word_weight_list.append(i/float(weight_sum))
        word_weight_list.append(normalize_word_weight_list)
        word_vec_list.append(sentence_word_vec_list)
    return word_weight_list, word_vec_list

def shuffle(list1, list2, mode = 'load'):
    if mode == 'load' and os.path.exists('../data/perm.txt'):
        fr = open('../data/perm.txt')
        perm_str = fr.readline().strip().split(' ')
        perm = []
        for i in perm_str:
            perm.append(int(i))
    else:
        length = len(list1)
        perm = [i for i in range(length)]
        random.shuffle(perm)
        perm_str = []
        for i in perm:
            perm_str.append(str(i))
        fw = open('../data/perm.txt', 'w')
        fw.write(' '.join(perm_str))
        fw.close()
    new_list1 = []
    new_list2 = []
    for  i in perm:
        new_list1.append(list1[i])
        new_list2.append(list2[i])
    return new_list1, new_list2

def cosine_distance(f1, f2):
    result = cosine_similarity([f1], [f2])
    r = float(result[0][0])
    return r

if __name__=='__main__':
    rate = 0.1
    k = 9
    label_list, twitter_list = load_all_data()
    label_list, twitter_list = shuffle(label_list, twitter_list)
    total = len(label_list)
    t_len = int(rate*total)
    idf_dict = cal_idf(twitter_list)
    load_word2vec_model()
    twitter_weight_array, twitter_vec_array = load_twitter_vec(twitter_list, idf_dict)
    
    test_vec =  twitter_vec_array[:t_len]
    test_weight = twitter_weight_array[:t_len]
    test_label = label_list[:t_len]
    test_title = twitter_list[:t_len]
    train_vec =  twitter_vec_array[t_len:]
    train_weight = twitter_weight_array[t_len:]
    train_label = label_list[t_len:]
    train_title = twitter_list[t_len:]

    p = 0.0
    for i in range(len(test_label)):
        d_list = []
        for j in range(len(train_label)):
            d = emd((test_vec[i], test_weight[i]), (train_vec[j], train_weight[j]), cosine_distance)
            d_list.append(d)
        l_list = []
        for n in range(k):
            temp = 0
            pos = -1
            for index,d in enumerate(d_list):
                if d > temp:
                    temp = d
                    pos = index
            l_list.append(train_label[pos])
            d_list[pos] = 0
        label, times = Counter(l_list).most_common(1)[0]
        print test_title[i] + '\t' + label + '\t' + test_label[i] + '\t' + ' '.join(l_list)
        if label == test_label[i]:
            p +=1
    print p
    print t_len
    print p/t_len
