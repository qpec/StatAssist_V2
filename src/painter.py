from src.Config import color_scheme, card_width
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
    paragraph_styles = getSampleStyleSheet()
    paragraph_styles.add(
        ParagraphStyle(
            name="Term",
            fontName="Helvetica-Bold",
            fontSize=22,
            alignment=TA_LEFT,
            textColor="black",
            leading=23,
    ))
    paragraph_styles.add(
        ParagraphStyle(
            name="What",
            fontName="Helvetica",
            fontSize=10.5,
            alignment=TA_JUSTIFY,
            textColor="black",
            leading=11,
    ))


    # access the content
    first_occurence = card_content["first"]
    first_page = card_content["first_page"]
    term = card_content["term"]
    what = '<b>What it is. </b>' + str(card_content["what"])
    important = '<b>Important. </b>' + str(card_content["important"])
    image = card_content["image"]

    # development
    dummy = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.'

    term_paragraph = Paragraph(str(term), paragraph_styles["Term"])
    what_paragraph = Paragraph(str(what), paragraph_styles["What"])
    #for development (when important is empty)
    if not isna(important):
        imp_paragraph = Paragraph(str(important), paragraph_styles["What"])
    else:
        imp_paragraph = Paragraph(str(dummy), paragraph_styles["What"])

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

    data = []
    if not first_occurence:
        second_occur = 'for <b>' + term + "</b> see page " + str(first_page+1)
        second_occur_paragraph = Paragraph(second_occur, paragraph_styles["What"])
        data.append([second_occur_paragraph])
    else:
        data.append([term_paragraph])
        data.append([what_paragraph])
        if imp_paragraph:
            data.append([imp_paragraph])
        '''if image:
            data.append(['', image])'''

    back_col = colors.HexColor(color_scheme['back_col'])
    fore_col = colors.HexColor(color_scheme['fore_col'])
    text_col = colors.HexColor(color_scheme['text_col'])
    textfade_col = colors.HexColor(color_scheme['textfade_col'])
    high1full_col = colors.HexColor(color_scheme['high1full_col'])
    high1fade_col = colors.HexColor(color_scheme['high1fade_col'])
    high2full_col = colors.HexColor(color_scheme['high2full_col'])
    high2fade_col = colors.HexColor(color_scheme['high2fade_col'])

    card = Table(
        data,
        colWidths=(card_width),
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), fore_col),
            ("BOX", (0, 0), (-1, -1), 10, fore_col),
            ("LEFTPADDING", (0, 0), (0, -1), 8),
            ("TOPPADDING", (0, 0), (0, 0), 4),
            ("BOTTOMPADDING", (0, -1), (0, -1), 8),
            ("RIGHTPADDING", (0,0), (0,-1), 8),
        ],
    )
    return card
