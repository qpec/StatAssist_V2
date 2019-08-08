from src.translator import translate_for_narration
import pandas as pd

"""
should format information into a card containing:
 ___________________________
|3 found matches    on page |--> equal to the len of index in dict
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

"""


def narrate_translation(pdf_path, excel_path):
    statguide = pd.read_excel(excel_path)
    statguide_columns = statguide.columns
    term_column = statguide_columns[0]
    category_column = statguide_columns[2]
    what_column = statguide_columns[2]
    important_column = statguide_columns[6]
    image_column = statguide_columns[4]

    page_highlights = []
    page_cards_content = []

    translation = translate_for_narration(pdf_path, excel_path)
    for page_i in range(len(translation)):
        page = translation[page_i]
        this_page_highlights = []
        this_page_cards_content = []

        for term_index in page:
            plotitems = page[term_index]

            title_term_carditem = statguide[term_column][term_index]
            category_carditem = statguide[category_column][term_index]
            what_carditem = statguide[what_column][term_index]
            important_carditem = statguide[important_column][term_index]
            image_carditem = statguide[image_column][term_index]

            coordinates = []
            fo = []
            for plotitem in plotitems:
                fo.append(plotitem[1])
                coordinates.append(plotitem[3])
            highlights = list(zip(fo, coordinates))

            '''this here checks if any highlight in the searchindex is True,
            meaning, it is a first page occurence'''
            if any(fo):
                first_occurence = True
            else:
                first_occurence = False

            first_page = plotitems[0][2]

            # Here the formatting for the output card and highlight gets established
            term_card_content = {
                'first': first_occurence,
                'first_page': first_page,
                'term': title_term_carditem,
                'what': what_carditem,
                'important': important_carditem,
                'image': image_carditem,
            }
            this_page_highlights.append(highlights)
            this_page_cards_content.append(term_card_content)
        page_highlights.append(this_page_highlights)
        page_cards_content.append(this_page_cards_content)

    return page_cards_content, page_highlights
