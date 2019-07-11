'''This class acts as the art director of the package. It uses the painter to
create the elements required for the sidebar and generates a highlighted pdf'''

from src.Config import excel_path, pdf_path, output_pdf_path
from src.narrator import narrate_translation
#from src.painter import paint_card
from reportlab.platypus import Spacer, Frame
from reportlab.pdfgen.canvas import Canvas

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

    data = [
        ["", term_paragraph],
        ["", what_paragraph],
    ]
    #for development if important not in cell
    if imp_paragraph:
        data.append(["", imp_paragraph])
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
        colWidths=(4, card_width),
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), fore_col),
            ("BOX", (0, 0), (-1, -1), 12, fore_col),
            ("BACKGROUND", (0, 0), (0, -1), high1full_col),
            ("LEFTPADDING", (1, 0), (1, -1), 2),
            ("TOPPADDING", (1, 0), (1, 0), 1),
            ("BOTTOMPADDING", (1, -1), (1, -1), 8),
            ("RIGHTPADDING", (1,0), (1,-1), 6),
        ],
    )
    return card

def sketch_blueprints(pdf_path, excel_path):
    narrative = narrate_translation(pdf_path, excel_path)
    highlights_per_page_areas = []
    cards_per_page_content = []

    for page_i in range(len(narrative)):
        page_content = narrative[page_i]
        highlights_per_page_areas.append([term['term_highlights'] for term in page_content])
        cards_per_page_content.append([term['term_card_content'] for term in page_content])

    return highlights_per_page_areas, cards_per_page_content


def article_highlighter():
    pass


def build_blueprint(pdf_path, excel_path, output_pdf_path, pdf_name='pdf_name.pdf'):
    highlights_per_page_areas, cards_per_page_content = sketch_blueprints(pdf_path, excel_path)

    c = Canvas(output_pdf_path + pdf_name, pagesize=(1000, 2000))
    sidebar = Frame(100,100,300,1000)

    for page_i in range(len(cards_per_page_content)):
        sidebar_story_page = []
        for card_content in cards_per_page_content[page_i]:
            this_card = paint_card(card_content)
            sidebar.add(this_card, c)
            sidebar.add(Spacer(10,20), c)
        c.showPage()

    c.save()

build_blueprint(pdf_path, excel_path, output_pdf_path)
