#coding=utf-8
def eva(filepath):
    fr = open(filepath)
    count = 0
    total = 0
    for line in fr.readlines():
        array = line.strip().split('\t')
        if '\t' not in line or len(array) != 3:
            continue
        y_list = array[2].strip().split(',')
        y = array[1]
        total += 1
        if y in y_list:
            count += 1
    print filepath, count, total, float(count)/total

if __name__=='__main__':
    eva('idf.res')
    eva('raw.res')
