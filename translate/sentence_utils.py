#coding=utf-8
import os
import random
def create_vocab():
    word_set = set()
    raw_data_path = 'data/raw-data.csv'
    vocab_path = 'gen/vocab.txt'
    fr = open(raw_data_path)
    fw = open(vocab_path, 'w')
    for line in fr.readlines():
        sentence = line.strip()
        if sentence == '':
            continue
        word_list = sentence.split(' ')
        for word in word_list:
            if word not in word_set:
                word_set.add(word)
                fw.write(word + '\n')
    fr.close()
    fw.close()

def split():
    fr = open('data/raw-data.csv')
    content = fr.readlines()
    for i in range(3):
        random.shuffle(content)
    fw = open('gen/train.txt', 'w')
    for line in content[:-300]:
        fw.write(line)
    fr.close()
    fw.close()
    fw = open('gen/test.txt', 'w')
    for line in content[-300:]:
        fw.write(line)
    fw.close()

if __name__=='__main__':
    split()
