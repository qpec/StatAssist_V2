'''This module modifies matcher results to be implemented for the
narrator module. It specifies on which pages terms occur and where
said term is located'''

from src.matcher import get_articledict_and_matchesdict

def remove_duplicates_list(lst):
    clean_list = []
    for item in lst:
        if item not in clean_list:
            clean_list.append(item)
    return clean_list

def get_highlight_boxes_pp(article_dict):
    coordinates = article_dict["coordinates"]
    total_pages = article_dict["total_pages"]
    wordindex_to_page = article_dict["pages"]
    matches = article_dict["matches"]

def cord_evaluator(coordinate_list):
    # Coordinates are: x1, y1, x2, y2
    y_deviation = False
    if len(coordinate_list)>1:
        x1 = []
        x2 = []
        y1 = []
        y2 = []
        for cords in coordinate_list:
            x1.append(cords[0])
            x2.append(cords[2])
            y1.append(cords[1])
            y2.append(cords[3])
        if y1[0] != y1[-1]:
            y_deviation = True
        if y_deviation:
            # here can insert function that evaluates initial
            # two words or more that are on the same line
            return coordinate_list
        else:
            new_cords = [(min(x1), min(y1), max(x2), max(y2))]
            return new_cords
    else:
        return coordinate_list


def translate_for_narration(pdf_path, excel_path):
    article_dict, search_term_index_vector = get_articledict_and_matchesdict(
            pdf_path, excel_path)
    words = article_dict["words"]
    coordinates = article_dict["coordinates"]
    total_pages = article_dict["total_pages"]
    page_matches = article_dict["page_matches"]
    matches = article_dict["matches"]
    first_occurences = article_dict["first"]
    # translation has structure: {'search_term_index':(fo, cords)}
    translation = [{} for i in range(total_pages+1)]
    for i in range(len(matches)):
        match = matches[i]

        # get the article match (only for debugging)
        article_match = []
        for index in match:
            article_match.append(words[index])
        article_match = " ".join(article_match)

        # get the index of the term in the searchquery
        search_match = article_dict["index_searchterms"][i]
        # check if this is the first_occurence
        fo = first_occurences[i]
        # get the coordinates of bbox of specified term

        cords = []
        for index in match:
            cords.append(coordinates[index])

        article_match = []
        for index in match:
            article_match.append(words[index])

        this_match_page_matches = page_matches[i]
        unique_pages = remove_duplicates_list(this_match_page_matches)
        multiple_pages = False
        if len(unique_pages) > 1:
            multiple_pages == True

        # here it is taken into account that it is possible that a term
        # is split up to multiple pages plotpoint get split
        if multiple_pages:
            for page in range(len(this_match_page_matches)):
                plotitem = (article_match[i][page], fo, cords[i][page])
                if search_match not in translation[page]:
                    translation[page][search_match] = [plotitem]
                else:
                    translation[page][search_match].append(plotitem)
        else:
            page = this_match_page_matches[0]
            cords = cord_evaluator(cords)
            article_match = " ".join(article_match)
            plotitem = (article_match, fo, cords)
            if search_match not in translation[page]:
                translation[page][search_match] = [plotitem]
            else:
                translation[page][search_match].append(plotitem)
    # translation has structure: {'search_term_index':(fo, cords)}
    # with multiple dictionaries, indexed to page
    return translation
