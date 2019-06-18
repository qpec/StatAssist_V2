import re
from nltk.stem import SnowballStemmer
from unidecode import unidecode
import fitz

def cleaner(text):
    text = text.lower()
    text = unidecode(text)
    text = re.sub(r'-\n', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\'', '', text)
    text = re.sub(r'[^a-zA-Z0-9\<\>]', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text

def term_query_cleanerstemmer(input_text, stem=True):
    '''when entering string, becomes list.
    always outputs list'''
    if not isinstance(input_text, list):
        input_text = list(input_text)
    output_text = []
    if stem:
        stemmer = SnowballStemmer('english')
    for item in input_text:
        output_item = []
        for subitem in item:
            text = cleaner(subitem)
            if stem:
                text_stemmed = " ".join([stemmer.stem(word) for word in text.split()])
                output_item.append(text_stemmed)
            else:
                output_item.append(text)
        output_text.append(output_item)
    return output_text

def txt_pages_cleanerstemmer(text_pages, stem):
    if stem:
        stemmer = SnowballStemmer('english')
    output_text_pages = []
    for page in text_pages:
        text = cleaner(page)
        if stem:
            text_stemmed = " ".join([stemmer.stem(word) for word in text.split()])
            output_text_pages.append(text_stemmed)
        else:
            output_text_pages.append(text)
    return output_text_pages

def return_pdf_text_pp(pdf_path):
    text_pp = []
    pdf_object = fitz.Document(pdf_path)
    for page in pdf_object:
        text_pp.append(page.getText())
    pdf_object.close()
    return text_pp
