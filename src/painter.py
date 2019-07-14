from src.Config import color_scheme, sidebar_width, margins
from src.narrator import narrate_translation
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tables import Table
from reportlab.lib import colors, utils
from pandas import isna

def paint_card(card_content):
    # instantiate color configurations etc
    back_col = colors.HexColor(color_scheme['back_col'])
    fore_col = colors.HexColor(color_scheme['fore_col'])
    text_col = colors.HexColor(color_scheme['text_col'])
    textfade_col = colors.HexColor(color_scheme['textfade_col'])
    high1full_col = colors.HexColor(color_scheme['high1full_col'])
    high1fade_col = colors.HexColor(color_scheme['high1fade_col'])
    high2full_col = colors.HexColor(color_scheme['high2full_col'])
    high2fade_col = colors.HexColor(color_scheme['high2fade_col'])

    paragraph_styles = getSampleStyleSheet()
    paragraph_styles.add(
        ParagraphStyle(
            name="Term",
            fontName="Helvetica-Bold",
            fontSize=22,
            alignment=TA_LEFT,
            textColor=text_col,
            leading=23,
    ))
    paragraph_styles.add(
        ParagraphStyle(
            name="What",
            fontName="Helvetica",
            fontSize=10.5,
            alignment=TA_JUSTIFY,
            textColor=text_col,
            leading=11,
    ))
    paragraph_styles.add(
        ParagraphStyle(
            name="Repeat",
            fontName="Helvetica",
            fontSize=10.5,
            alignment=TA_LEFT,
            textColor=text_col,
            leading=11,
    ))


    # access the content
    # Card 1
    first_occurence = card_content["first"]
    first_page = card_content["first_page"]
    term = card_content["term"]
    what = str(card_content["what"])
    important = card_content["important"]
    image = card_content["image"]

    term_paragraph = Paragraph(str(term), paragraph_styles["Term"])
    what_paragraph = Paragraph(str(what), paragraph_styles["What"])
    #for development (when important is empty)
    if not isna(important):
        imp_paragraph = Paragraph(str('<img src="input/inline_images/exclamation.png" valign=-1.5 width=10.5 height=10.5 /> ' + important), paragraph_styles["What"])
    else:
        imp_paragraph = False


    # Card 2
    second_occur = 'Click here for <b>' + term + "</b> on page " + str(first_page+1)
    second_occur_paragraph = Paragraph(second_occur, paragraph_styles["Repeat"])

    #later implementation of image carditem
    '''if not isna(image):
        print(image)
        image_path = "input/images/" + image + ".png"
        img_object = utils.ImageReader(image_path)
        iw, ih = img_object.getSize()
        aspect = ih / float(iw)
        wid = card_width*0.8
        image = Image(image_path, width=wid, height=wid*aspect)
    else:
        image = '''



    card_data = []
    card_styling=[
        ("BACKGROUND", (0, 0), (-1, -1), fore_col),
        ("VALIGN", (0, 0), (-1, 0), "TOP"),
        ("LEFTPADDING", (2, 0), (2, -1), 8),
        ("TOPPADDING", (2, 0), (2, 0), 4),
        ("BOTTOMPADDING", (2, -1), (2, -1), 7),
        ("RIGHTPADDING", (2,0), (2,-1), 8)]

    column_1_2_width = 5
    if not first_occurence:
        card_styling.append(("BOX", (0, 0), (-1, -1), 10, fore_col))
        card_data.append(['', '', second_occur_paragraph])
        column_1_2_width = 0
    else:
        card_styling.append(("BACKGROUND", (1, 0), (1, -1), high2full_col))
        card_styling.append(("BOX", (0, 0), (-1, -1), 10, fore_col))
        card_data.append(['', '', term_paragraph])
        card_data.append(['', '', what_paragraph])
        if imp_paragraph:
            card_data.append(['', '', imp_paragraph])
        '''if image:
            card_data.append(['', '', '', image])'''

    card = Table(
        card_data,
        colWidths=(column_1_2_width, column_1_2_width, sidebar_width - margins - 2*column_1_2_width),
        style=card_styling
    )
    return card
