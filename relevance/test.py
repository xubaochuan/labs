#coding=utf-8
import utility
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity

def read_file(filepath):
    fr = open(filepath)
    content = fr.read()
    fr.close()
    return content

if __name__=='__main__':
    filepath = 'data/r.txt'
    content = read_file(filepath)
    sentence_list, sentence_vec_list = utility.get_sentence_vec(content)
    keywords = "interfacial energy; anisotropy; equilibrium shape"
    keyword_list, keyword_vec_list = utility.get_sentence_vec(keywords, 0)
    distance = cosine_similarity(keyword_vec_list, sentence_vec_list)
    for i,keyword in enumerate(distance):
        print "related to " + keyword_list[i] + ':'
        for j,d in enumerate(distance[i]):
            if d > 0.3:
                print sentence_list[j],d

