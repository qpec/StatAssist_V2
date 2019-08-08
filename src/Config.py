import os

excel_path = os.path.abspath("input/StatGuide.xlsx")
pdf_path = os.path.abspath("input/example.pdf")
output_pdf_path = os.path.abspath("output/")

highlight_margin = 1

color_scheme = {
    'back_col':'#262626',
    'fore_col':'#ffffff',
    'text_col':'#262626',
    'textfade_col':'#999999',
    'high1full_col':'#3797f0',
    'high1fade_col':'#E8A78B',
    'high2full_col':'#FAA629',
    'high2fade_col':'#e6e6e6',
    'old_col1':'#EC4E3C',
    'old_col2':'#FFC638',
}

#these variables are associated with the sidebar and flowable_classes
card_width = 250
sidebar_width = 275
a4_width = 595
a4_height = 842
margins = 8
