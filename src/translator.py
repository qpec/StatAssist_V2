'''This module modifies matcher results to be implemented for the
narrator module. It specifies on which pages terms occur and where
said term is located'''

from src.Config import excel_path, pdf_path
from src.matcher import get_articledict_and_matchesdict


def get_highlight_boxes_pp(article_dict):
    coordinates = article_dict["coordinates"]
    total_pages = article_dict["total_pages"]
    wordindex_to_page = article_dict["pages"]
    matches = article_dict["matches"]


def translate_for_narration(pdf_path, excel_path):
    article_dict, search_term_index_vector = get_articledict_and_matchesdict(
            pdf_path, excel_path)
    words = article_dict["words"]
    coordinates = article_dict["coordinates"]
    total_pages = article_dict["total_pages"]
    wordindex_to_page = article_dict["pages"]
    matches = article_dict["matches"]
    print(matches)
    first_occurence = article_dict["first"]

    narrative = []
    for match in matches:
        # get the index of the term in the searchquery
        term = []
        for index in match:
            term.append(words[index])
        term = " ".join(term)
        search_term_index = search_term_index_vector[term]

        # get the coordinates of bbox of specified term
        term_cords = []
        for index in match:
            term_cords.append(coordinates[index])


translate_for_narration(pdf_path, excel_path)
