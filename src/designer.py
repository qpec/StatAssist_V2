'''This class acts as the art director of the package. It uses the painter to
create the elements required for the sidebar and generates a highlighted pdf'''

from src.Config import excel_path, pdf_path, output_pdf_path, sidebar_width, a4_width, a4_height, margins, card_width, color_scheme
from src.narrator import narrate_translation
from src.painter import paint_card
from reportlab.platypus import Spacer, Frame
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors

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
    textfade_col = colors.HexColor(color_scheme['textfade_col'])
    high1full_col = colors.HexColor(color_scheme['high1full_col'])
    high1fade_col = colors.HexColor(color_scheme['high1fade_col'])
    high2full_col = colors.HexColor(color_scheme['high2full_col'])
    high2fade_col = colors.HexColor(color_scheme['high2fade_col'])

    page_cards_content, page_highlights = narrate_translation(pdf_path, excel_path)

    full_page_width = a4_width + sidebar_width + 3*margins
    c = Canvas(output_pdf_path + pdf_name, pagesize=(full_page_width, a4_height+2*margins))
    for page_i in range(len(page_cards_content)):
        # necessary for link to this page
        c.bookmarkPage(page_i)

        # sidebar background color
        c.setFillColor(text_col)
        c.rect(0, 0, a4_width + sidebar_width + 3*margins, a4_height+2*margins, stroke=0, fill=1)
        sidebar = Frame(full_page_width - sidebar_width - margins*1.5, margins, sidebar_width, a4_height-margins, showBoundary=1)
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
            sidebar.add(Spacer(10,15), c)
        c.showPage()

    c.save()

build_blueprint(pdf_path, excel_path, output_pdf_path)
