#coding=utf-8
def analyze(filepath):
    bow = set()
    fr = open(filepath)
    n = 0
    uniq_count = 0
    for line in fr.readlines():
        array = line.strip().split('\t')
        if '\t' not in line or len(array) != 2:
            continue
        n += 1
        example = set()
        content = array[1]
        words = content.strip().split(' ')
        for word in words:
            if word not in bow:
                bow.add(word)
            if word not in example:
                example.add(word)
        uniq_count += len(example)
    print filepath, n, len(bow), float(uniq_count)/n

if __name__=='__main__':
    filepaths = ['twitter/data/data2.txt', 'bbcsport/data/data.txt', 'common/20news/data.txt', 'common/reuters/data.txt']
    for filepath in filepaths:
        analyze(filepath)
