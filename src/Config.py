import os

excel_path = os.path.abspath("input/StatGuide.xlsx")
pdf_path = os.path.abspath("input/test.pdf")
output_pdf_path = os.path.abspath("output/")

color_scheme = {
    'back_col':'#282c35',
    'fore_col':'#edeff1',
    'text_col':'#282c35',
    'textfade_col':'#3b4c54',
    'high1full_col':'#ED6D23',
    'high1fade_col':'#E8A78B',
    'high2full_col':'#FAA629',
    'high2fade_col':'#F7CA94',
}

#these variables are associated with the sidebar and flowable_classes
card_width = 250
