from src.Config import excel_path, pdf_path
from src.translator import translate_for_narration
import pandas as pd

'''
should format information into a card containing:
 ___________________________
|3 found occurences on page |--> equal to the len of index in dict
|                           |
|P value(1)   (2)INFERENTIAL|-->(1) found in [1] (2) in [4]
|What is it: Threshold value|-->found in excel dictionary [2]
|indicating theoretical prob|
|that results are truely ran|
|                           |
|Important: the p-value does|-->found in excel dictionary [3]
|not translate to the clinic|
|IMAGE?                     |-->path to image found in [5]
|___________________________|

'''

def narrate_translation(pdf_path, excel_path):
    translation = translate_for_narration(pdf_path, excel_path)
    statguide = pd.read_excel(excel_path)
    narrative = [[] for page in translation]
    for page in translation:
        for term in page:
            term = page[term]
            found_occurences = len(term)
            occurences_card_item = str(found_occurences) + "matches for"


narrate_translation(pdf_path, excel_path)
