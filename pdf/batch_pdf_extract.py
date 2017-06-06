#coding=utf-8
import os
import pdf_extract
import hashlib

def get_md5_value(s):
    myMd5 = hashlib.md5()
    myMd5.update(s)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def get_file_md5(filename):
    fd = open(filename,"r")
    fcont = fd.read()
    fd.close()
    fmd5 = hashlib.md5(fcont)
    return fmd5.hexdigest()

if __name__=='__main__':
    n = '2'
    filedir = 'part' + n
    filenames = os.listdir(filedir)
#    id_title_fw = open('id_title.txt', 'w')
#    id_content_fw = open('id_content.txt', 'w')
    all_info_fw = open('all_info_part_' + n +'.txt', 'w')
    wordvec_fw = open('wordvec_data_part_' + n +'.txt', 'w')
    for index,name in enumerate(filenames):
        print name
        filepath = os.path.join(filedir, name)
        text_list = pdf_extract.get_pdf_text(filepath)
        title = name.replace('.pdf', '')
        title_md5 = get_md5_value(title)
        file_md5 = get_file_md5(filepath)
        all_info_fw.write(str(index) + '\t' + title + '\t' + title_md5 + '\t' + file_md5 + '\t' + '. '.join(text_list) + '\n')
        wordvec_fw.write('\n'.join(text_list))
    all_info_fw.close()
    wordvec_fw.close()
