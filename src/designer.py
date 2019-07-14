'''This class acts as the art director of the package. It uses the painter to
create the elements required for the sidebar and generates a highlighted pdf'''

from src.Config import excel_path, pdf_path, output_pdf_path, sidebar_width, a4_width, a4_height, margins, card_width, color_scheme
from src.narrator import narrate_translation
from src.painter import paint_card
from reportlab.platypus import Spacer, Frame
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from io import StringIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.graphics.shapes import Rect
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from pdfrw import PdfReader

def article_highlighter():
    pass


def add_page_link(page_to_link_to, y1, y2, canvas):
    link_x1 = a4_width + margins*2
    box = (link_x1, y1, link_x1 + card_width, y2)
    tooltip = 'Go to page ' + str(page_to_link_to)
    canvas.linkAbsolute(tooltip, page_to_link_to, Rect=box)
    return


def build_blueprint(pdf_path, excel_path, output_pdf_path, pdf_name='pdf_name.pdf'):
    back_col = colors.HexColor(color_scheme['back_col'])
    fore_col = colors.HexColor(color_scheme['fore_col'])
    text_col = colors.HexColor(color_scheme['text_col'])
    white = colors.white
    textfade_col = colors.HexColor(color_scheme['textfade_col'])
    high1full_col = colors.HexColor(color_scheme['high1full_col'])
    high1fade_col = colors.HexColor(color_scheme['high1fade_col'])
    high2full_col = colors.HexColor(color_scheme['high2full_col'])
    high2fade_col = colors.HexColor(color_scheme['high2fade_col'])

    # import the required content/highlight locations
    page_cards_content, pages_highlights = narrate_translation(pdf_path, excel_path)


    # instantiate visual object of original article to highlight with rects
    original_article = PdfReader(pdf_path)
    original_article_pages = [page for page in original_article.pages]
    c = Canvas(output_pdf_path + pdf_name, pagesize=(a4_width + sidebar_width + (3*margins), a4_height+(2*margins)))

    for page_i in range(len(page_cards_content)):
        # draw background1
        c.setFillColor(back_col)
        c.rect(0, 0, a4_width + sidebar_width + 3*margins, a4_height+2*margins, stroke=0, fill=1)
        # draw white canvas for pdf
        c.setFillColor(white)
        c.roundRect(margins, margins, a4_width, a4_height, 5, stroke=0, fill=1)
        # draw black canvas for frame sidebar
        c.setFillColor(back_col)
        c.rect(a4_width + 2*margins, margins, sidebar_width, a4_height, stroke=0, fill=1)
        # sidebar frame
        sidebar = Frame(a4_width + 2*margins, margins, sidebar_width, a4_height, showBoundary=1)
        # first paste the original pdf on the canvas
        original_article_page = pagexobj(original_article_pages[page_i])
        #c.doForm(makerl(c, original_article_page))

        ''' this part deals with the highlight elements'''
        for highlight in pages_highlights[page_i]:
            highlight = highlight[0]
            first = highlight[0]
            cords = highlight[1]
            x1 = cords[0]
            y1 = cords[1]
            x2 = cords[2]
            y2 = cords[3]
            if first:
                c.setFillColor(high2full_col)
            else:
                c.setFillColor(high2fade_col)
            c.roundRect(x1,y1,x2-x1,y2-y1,1, fill=True, stroke=False)
        c.doForm(makerl(c, original_article_page))
        '''this part deals with the sidebar elements'''
        # necessary for link to this page
        c.bookmarkPage(page_i)

        sidebar_story_page = []
        for card_content in page_cards_content[page_i]:
            this_card = paint_card(card_content)

            link_y = []
            if this_card._nrows <= 1:
                # this is a repeated term
                link_y.append(sidebar._y)
            sidebar.add(this_card, c)

            if link_y:
                link_y.append(sidebar._y)
                add_page_link(card_content['first_page'], link_y[0], link_y[1], c)
                link_y.clear()
            sidebar.add(Spacer(10, margins + 10), c)
        c.showPage()

    c.save()

build_blueprint(pdf_path, excel_path, output_pdf_path)
