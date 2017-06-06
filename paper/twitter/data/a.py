fr = open('data.txt')
for line in fr.readlines():
    array = line.strip().split('\t')
    if '\t' not in line:
        continue
    words = array[1].split(' ')
    if len(words) > 4:
        print line.strip()
