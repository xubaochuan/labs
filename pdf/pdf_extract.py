#coding=utf-8
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal
import re
import unicodedata

invalid_strings = ['Corresponding authors', 'E-mail addresses', 'corresponding authors', 'e-mail address']

def remove_references(text_list):
    pattern = re.compile(r'^\[\d+\]')
    temp_line = 0
    for i in range(len(text_list),0,-1):
        match = pattern.match(text_list[i-1])
        if match and '.' in text_list[i-1]:
            if temp_line == 1:
                del text_list[i]
                temp_line = 0
            del text_list[i-1]
        else:
            if temp_line == 1:
                break
            else:
                temp_line = 1
    return text_list

def conv_ligature(string):
    conv_ligature_string = unicodedata.normalize("NFKD", string.decode('utf-8'))
    return conv_ligature_string.encode('utf-8')

def get_pdf_text(filepath):
    fp = open(filepath, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTestExtractionNotAllowed

    rsrmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrmgr, device)
    i = 0
    content_list = []
    for page in PDFPage.create_pages(document):
        i += 1
        interpreter.process_page(page)
        layout = device.get_result()
        j = 0
    
        filter_layout = []
        for x in layout:
            if isinstance(x, LTTextBoxHorizontal):
                text = x.get_text().encode('utf-8')
                if text.strip().isdigit():
                    continue
                else:
                    filter_layout.append(x)

        num = len(filter_layout)
        for x in filter_layout:
            if isinstance(x, LTTextBoxHorizontal):
                j += 1
                if i == 1 and j < 5:
                    continue
                if i == 1 and j == num:
                    continue
                if i > 1 and j == 1:
                    continue
                text = x.get_text().encode('utf-8')
                invalid_flag = 0
                for string in invalid_strings:
                    if string in text:
                        invalid_flag = 1
                        break
                if invalid_flag == 1:
                    continue
            
                if text.count('. ') == 1 and text.count('\n') == 1:
                    number_str = text.strip().split('. ')[0]
                    number_list = number_str.strip().split('.')
                    sub_title_flag = 1
                    for n in number_list:
                        if not n.isdigit():
                            sub_title_flag = 0
                            break
                    if sub_title_flag == 1:
                        content_list.append(text.replace('\n', ''))
                        continue
                text_list = text.strip().split('\n')
                if len(text)/len(text_list) > 50:
                    content_list.append(text.replace('\n', ''))
    fp.close()
    for text in content_list:
        text = conv_ligature(text)
    content_list = remove_references(content_list)
    return content_list
