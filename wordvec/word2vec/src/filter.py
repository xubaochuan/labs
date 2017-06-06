#coding=utf-8
fr = open('data/lishi.txt')
fw = open('data/lishi.n.txt', 'w')
word_dict = {}
for line in fr.readlines():
    if ' ' not in line:
        continue
    line_list = line.strip().split(' ')
    if '/' not in line_list[0]:
        continue
    classes = line_list[1]
    word_list = line_list[0].strip().split('/')
    word = word_list[0]
    tag = word_list[1]
    if 'n' in tag and tag[0] == 'n':
        if len(word) == 3:
            continue
        if classes not in word_dict:
            word_dict[classes] = []
        word_dict[classes].append(word)
for key,words in word_dict.items():
    if len(words) <=5 :
        continue
    line = ' '.join(words)
    fw.write(line + '\n')
fw.close()
fr.close()
