from src.Config import excel_path, pdf_path
from src.narrator import narrate_translation
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (Flowable, Paragraph,
                                SimpleDocTemplate, Spacer)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

"""
should format information into a card containing:
 ___________________________
|3 found matches    on page |--> equal to the len of index in dict
|                           |
|P value(1)   (2)INFERENTIAL|-->(1) found in [1] (2) in [4]
|What is it: Threshold value|-->found in excel dictionary [2]
|indicating theoretical prob|
|that results are truely ran|
|                           |
|Important: the p-value does|-->found in excel dictionary [3]
|not translate to the clinic|
|IMAGE?                     |-->path to image found in [5]
|___________________________|

"""

class CardMatches(Flowable):
    #----------------------------------------------------------------------
    def __init__(self, card_content, page, x=0, y=0, width=200, height=200):
        Flowable.__init__(self)
        self.vispage = page + 1
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle( name='pill',
                                        fontName='Helvetica',
                                        fontSize=9,
                                        alignment=TA_CENTER,
                                        leading=13,
                                        spaceAfter=3,
                                        spaceBefore=3,
                                        textColor="white",
                                        backColor="black",
                                        borderColor="black",
                                        borderPadding=1,
                                        borderWidth=2,
                                        #borderRadius=1
                                        ))

        len_matches = card_content['len_matches']
        category = card_content['category']
        term = card_content['term']
        what = card_content['what']
        important = card_content['important']
        image = card_content['image']

        markcolor = '#ff4ff2'

        self.matches_text = ""
        self.matches_text += str(len_matches)
        if len_matches > 1:
            self.matches_text += " matches on page "
        else:
            self.matches_text += " match on page "
        self.matches_text += str(self.vispage)



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

        p = Paragraph(self.matches_text, style=self.styles["pill"])
        p.wrapOn(self.canv, self.width, self.height)
        p.drawOn(self.canv, *self.coord(self.x, 0, mm))



def make_blueprints(pdf_path, excel_path):
    narrative = narrate_translation(pdf_path, excel_path)
    story=[]
    for i in range(len(narrative)-3):
        page_content = narrative[i]
        page_highlights = [term['term_highlights'] for term in page_content]
        page_cards = [term['term_card_content'] for term in page_content]
        doc = SimpleDocTemplate("test3.pdf",pagesize=letter)

        card = Card(page_cards[0], i)
        story.append(card)


    doc.build(story)

make_blueprints(pdf_path, excel_path)
