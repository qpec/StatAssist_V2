"""This module modifies matcher results to be implemented for the
narrator module. It specifies on which pages terms occur and where
said term is located"""
from src.Config import excel_path, pdf_path, output_pdf_path
from src.matcher import get_articledict_and_occurencetuple


def remove_duplicates_list(lst):
    clean_list = []
    for item in lst:
        if item not in clean_list:
            clean_list.append(item)
    return clean_list

def translate_for_narration(pdf_path, excel_path):
    article_dict, occurence_tuples = get_articledict_and_occurencetuple(
        pdf_path, excel_path
    )

    # from article dict
    words = article_dict["words"]
    coordinates = article_dict["coordinates"]
    total_pages = article_dict["total_pages"]

    # translation has structure: {'search_term_index':(fo, cords)}
    translations = [{} for i in range(total_pages+1)]
    for i in range(len(occurence_tuples)):
        search_match = occurence_tuples[i][0]
        article_match = occurence_tuples[i][1]
        first_occurence = occurence_tuples[i][2]
        page_first_occurence = occurence_tuples[i][3]
        this_page = occurence_tuples[i][4]

        # get the article match (only for debugging)
        article_string_match = []
        for index in article_match:
            article_string_match.append(words[index])
        article_string_match = " ".join(article_string_match)

        # get the coordinates of bbox of specified term
        cords = []
        for index in article_match:
            cords.append(coordinates[index])

        plotitem = (article_string_match, first_occurence, page_first_occurence, cords)

        if search_match not in translations[this_page]:
                translations[this_page][search_match] = [plotitem]
        else:
            translations[this_page][search_match].append(plotitem)
    # translation has structure: {'search_term_index':(fo, cords)}
    # with multiple dictionaries, indexed to page
    return translations

x=translate_for_narration(pdf_path, excel_path)
