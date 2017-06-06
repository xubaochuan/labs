#coding=utf-8
import sys
import nltk
import re
import word2vec
import time
import random
import os
import unicodedata

reload(sys)
sys.setdefaultencoding('utf8')

def sentence_tokenize(string):
    tokens = nltk.word_tokenize(string)
    return ' '.join(tokens)

def word2phrase(string):
    path = sys.path[0]
    filedir = 'temp'
    filename = 'temp_' + str(int(time.time())) + '_' + str(random.randint(0,100))
    filepath = os.path.join(path, filedir, filename)
    input_filepath = filepath + '.input'
    output_filepath = filepath + '.output'
    fw = open(input_filepath, 'w')
    fw.write(string)
    fw.close()
    os.system('/data1/xubaochuan/nlp/wordvec/word2vec/src/word2phrase -train ' + input_filepath + ' -output ' + output_filepath)
#    word2vec.word2phrase(input_filepath, output_filepath, verbose=True)
    fr = open(output_filepath)
    phrased_string = fr.read()
    fr.close()
    if os.path.isfile(input_filepath):
        os.remove(input_filepath)
    if os.path.isfile(output_filepath):
        os.remove(output_filepath)
    return phrased_string

def get_sentence_vec(content, threshold = 10):
    wordvec_size = 200
    model_path = 'model/phrases_wordvec200.bin'
    model = word2vec.load(model_path)
    vocab = model.vocab
    tokenized_string = sentence_tokenize(content)
    phrased_string = word2phrase(tokenized_string)
    if ';' not in phrased_string and '.' not in phrased_string and '?' not in phrased_string and '\n' not in phrased_string:
        segments = [phrased_string]
    else:
        segments = re.split('[.?;]', phrased_string)
    sentence_vec_list = []
    sentence_list = []
    for sentence in segments:
        wordvec_list = []
        wordvec_sum = [0 for i in range(wordvec_size)]
        words = sentence.strip().split(' ')
        if len(words) < threshold:
            continue
        for word in words:
            if word in vocab:
                try:
                    wordvec = model[word]
                except:
                    print word
                    continue
                wordvec_list.append(wordvec)
                wordvec_sum = [x+y for x, y in zip(wordvec_sum, wordvec)]
        length = len(wordvec_list)
        sentence_vec = [x/length for x in wordvec_sum]
        sentence_vec_list.append(sentence_vec)
        sentence_list.append(sentence)
    return sentence_list,sentence_vec_list

if __name__=='__main__':
    print get_sentence_vec('It is well known that the applications of magnesium alloys aresigniﬁcantly potential in automobile, aircraft, aerospace, and 3C in-dustries because of their low density, high specific strength, goodcas    tability and better damping capacity and so on.')
