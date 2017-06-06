#coding-utf-8
import nltk
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def tokenize(string):
    tokens = nltk.word_tokenize(string.decode('utf-8'))
    return ' '.join(tokens)

if __name__=='__main__':
    fr = open('wordvec_data.txt')
    for line in fr.readlines():
        tokenize_string = tokenize(line)
        try:
            print tokenize_string
        except:
            pass
    fr.close()
