import re
from nltk.stem import SnowballStemmer
from unidecode import unidecode
from Config import *
import io
import fitz
import pdfplumber

def get_plumber_pdf_txt_pp(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text_pp = []
        for page in pdf.pages:
            text_pp.append(page.extract_text(x_tolerance=0.5))
    return text_pp

def cleaner(text):
    text = text.lower()
    text = unidecode(text)
    text = re.sub(r'-\n', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\'', '', text)
    text = re.sub(r' +', ' ', text)
    return text

def get_pdf_text_pp(pdf_path):
    text_pp = []
    pdf_object = fitz.Document(pdf_path)
    for page in pdf_object:
        text_pp.append(page.getText())
    pdf_object.close()
    return text_pp
