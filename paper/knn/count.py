#coding=utf-8
import csv
filepath = '../data/twitter/full-corpus.csv'
fr = open(filepath)
reader = csv.reader(fr)
c_dict = {}
for array in reader:
    label = array[1]
    if label not in c_dict:
        c_dict[label] = 1
    else:
        c_dict[label] += 1
fr.close()
for k,v in c_dict.items():
    print k,v
