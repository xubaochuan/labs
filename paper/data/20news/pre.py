#coding=utf-8
import os
def main():
    labels = ['athletics', 'cricket', 'football', 'rugby', 'tennis']
    for label in labels:
        docs = os.listdir(label)
        for name in docs:
            doc_path = os.path.join(label, name)
            fr = open(doc_path)
            content = []
            for line in fr.readlines():
                line = line.strip()
                if line == '':
                    continue
                content.append(line)
            print label + '\t' + ' '.join(content)

if __name__=='__main__':
    main()
