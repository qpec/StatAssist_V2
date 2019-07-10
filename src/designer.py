from src.Config import excel_path, pdf_path
from src.narrator import narrate_translation
from src.flowable_classes import Card


def make_blueprints(pdf_path, excel_path):
    narrative = narrate_translation(pdf_path, excel_path)
    story=[]
    for page_i in range(len(narrative)):
        page_content = narrative[page_i]
        page_highlights = [term['term_highlights'] for term in page_content]
        page_cards = [term['term_card_content'] for term in page_content]

        doc = SimpleDocTemplate("test3.pdf",pagesize=letter)

        card = Card(page_cards[0], i)
        story.append(card)


    doc.build(story)

make_blueprints(pdf_path, excel_path)
