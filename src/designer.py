'''This class acts as the art director of the package. It uses the painter to
create the elements required for the sidebar and generates a highlighted pdf'''

from src.Config import excel_path, pdf_path, output_pdf_path
from src.narrator import narrate_translation
from src.painter import paint_card
from reportlab.platypus import Spacer, Frame
from reportlab.pdfgen.canvas import Canvas

def article_highlighter():
    pass


def build_blueprint(pdf_path, excel_path, output_pdf_path, pdf_name='pdf_name.pdf'):
    page_cards_content, page_highlights = narrate_translation(pdf_path, excel_path)

    c = Canvas(output_pdf_path + pdf_name, pagesize=(1000, 2000))
    sidebar = Frame(100,100,300,1000)

    for page_i in range(len(page_cards_content)):
        sidebar_story_page = []
        for card_content in page_cards_content[page_i]:
            this_card = paint_card(card_content)
            print(this_card.data)
            sidebar.add(this_card, c)
            sidebar.add(Spacer(10,20), c)
        c.showPage()

    c.save()

build_blueprint(pdf_path, excel_path, output_pdf_path)
