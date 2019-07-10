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
    translation = translate_for_narration(pdf_path, excel_path)
    statguide = pd.read_excel(excel_path)
    statguide_columns = statguide.columns
    term_column = statguide_columns[1]
    category_column = statguide_columns[2]
    what_column = statguide_columns[3]
    important_column = statguide_columns[0]
    image_column = statguide_columns[5]

    narrative = []

    for page in translation:
        this_page_narrative = []
        for term_index in page:
            terms = page[term_index]
            found_occurences = len(terms)

            occurences_carditem = found_occurences
            title_term_carditem = statguide[term_column][term_index]
            category_carditem = statguide[category_column][term_index]
            what_carditem = statguide[what_column][term_index]
            important_carditem = statguide[important_column][term_index]
            image_carditem = statguide[image_column][term_index]

            coordinates = []
            first_occurences = []
            for term in terms:
                first_occurences.append(term[1])
                coordinates.append(term[2])

            if any(first_occurences):
                first_page_occurrence = True
            else:
                first_page_occurrence = False

            # Here the formatting for the output card and highlight gets established
            term_card_content = {
                'first': first_page_occurrence,
                'len_matches': occurences_carditem,
                'term': title_term_carditem,
                'category': category_carditem,
                'what': what_carditem,
                'important': important_carditem,
                'image': image_carditem,
            }

            highlights = tuple(zip(first_occurences, coordinates))

            cardcontent_highlights = {
                'term_card_content': term_card_content,
                'term_highlights': highlights,
            }
            this_page_narrative.append(cardcontent_highlights)
        narrative.append(this_page_narrative)

    return narrative
