#coding=utf-8
import csv
filepath = './data/data.txt'
fr = open(filepath)
reader = csv.reader(fr)
c_dict = {}
for line in fr.readlines():
    array = line.strip().split('\t')
    if '\t' not in line :
        continue
    label = array[0]
    if label not in c_dict:
        c_dict[label] = 1
    else:
        c_dict[label] += 1
fr.close()
for k,v in c_dict.items():
    print k,v
