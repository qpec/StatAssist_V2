import os

excel_path = os.path.abspath("input/StatGuide.xlsx")
pdf_path = os.path.abspath("input/test.pdf")
output_pdf_path = os.path.abspath("output/")

color_scheme = {
    'back_col':'#B8B2A6',
    'fore_col':'#F6F4EA',
    'text_col':'#1F2226',
    'textfade_col':'#3b4c54',
    'high1full_col':'#ED6D23',
    'high1fade_col':'#E8A78B',
    'high2full_col':'#FAA629',
    'high2fade_col':'#F7CA94',
    'old_col1':'#EC4E3C',
    'old_col2':'#FFC638',
}

#these variables are associated with the sidebar and flowable_classes
card_width = 250
sidebar_width = 275
a4_width = 595
a4_height = 842
margins = 8
