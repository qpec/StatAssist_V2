from src.Config import excel_path, pdf_path
from src.narrator import narrate_translation
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (Flowable, Paragraph,
                                SimpleDocTemplate, Spacer)

class Card(Flowable):
    #----------------------------------------------------------------------
    def __init__(self, x=0, y=0, width=200, height=200, card_content):
        Flowable.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.styles = getSampleStyleSheet()
        self.len_matches = card_content['len_matches']
        self.term = card_content['term']
        self.category = card_content['category']
        self.what = card_content['what']
        self.image = card_content['image']

    #----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y

    #----------------------------------------------------------------------
    def draw(self):
        """
        Draw the shape, text, etc
        """
        # self.canv.rect(self.x, self.y, self.width, self.height)
        # self.canv.line(self.x, 0, 500, 0)

        p = Paragraph(self.text, style=self.styles["Normal"])
        p.wrapOn(self.canv, self.width, self.height)
        p.drawOn(self.canv, *self.coord(self.x+2, 10, mm))
        p = Paragraph("<font size=20>This is a 10 point font</font><br/>jahoor", style=self.styles["Normal"])
        p.wrapOn(self.canv, self.width, self.height)
        p.drawOn(self.canv, *self.coord(self.x+2, 10, mm))


def make_blueprints(pdf_path, excel_path):
    narrative = narrate_translation(pdf_path, excel_path)
    for i in range(len(narrative)):
        page_content = narrative[i]
        page_highlights = [term['term_highlights'] for term in page_content]
        page_cards = [term['term_card_content'] for term in page_content]
        doc = SimpleDocTemplate("test3.pdf",pagesize=letter)
        story=[]

        box = BoxyLine(page_cards[0])
        story.append(box)


        doc.build(story)

make_blueprints(pdf_path, excel_path)
