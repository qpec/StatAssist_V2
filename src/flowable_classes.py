from src.Config import excel_path, pdf_path
from src.narrator import narrate_translation
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tables import Table
from reportlab.lib import colors

class Card(Flowable):
    # ----------------------------------------------------------------------
    def __init__(self, card_content, page, x=0, y=0, width=200, height=200):
        Flowable.__init__(self)
        self.vispage = page + 1
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.styles = getSampleStyleSheet()
        self.styles.add(
            ParagraphStyle(
                name="Term",
                fontName="Helvetica-Bold",
                fontSize=22,
                alignment=TA_LEFT,
                textColor="black",
                leading=23,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="What",
                fontName="Helvetica",
                fontSize=10.5,
                alignment=TA_JUSTIFY,
                textColor="black",
                leading=11,
            )
        )
        blue_highlight = colors.HexColor("#3b467e")
        red_highlight = colors.HexColor("#fe3742")
        # len_matches = card_content['len_matches']
        # category = card_content['category']
        term = card_content["term"]
        what = card_content["what"]
        important = card_content["important"]
        image = card_content["image"]
        self.term_paragraph = Paragraph(term, self.styles["Term"])
        self.what_paragraph = Paragraph(
            "<b>What is it. </b>The bladiebla equals a parameter that needs no further explanation, so this is oke like this.",
            self.styles["What"],
        )
        self.imp_paragraph = Paragraph(
            "<b>Important. </b>The bladiebla equals a parameter that needs no further explanation, so this is oke like this.",
            self.styles["What"],
        )

    # ----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height - y * unit
        return x, y

    # ----------------------------------------------------------------------
    def draw(self):
        """
        Draw the shape, text, etc
        """
        blue_highlight = colors.HexColor("#3b467e")
        red_highlight = colors.HexColor("#fe3742")
        card_white = colors.HexColor("#ffffff")
        back_white = colors.HexColor("#f3f4ef")

        data = [
            ["", self.term_paragraph],
            ["", self.what_paragraph],
            ["", self.imp_paragraph],
            ["", ""],
        ]

        t = Table(
            data,
            colWidths=(4, 240),
            style=[
                ("BACKGROUND", (0, 0), (-1, -1), back_white),
                ("BACKGROUND", (0, 0), (0, -1), blue_highlight),
                ("LEFTPADDING", (1, 0), (1, -1), 10),
                ("TOPPADDING", (1, 0), (1, 0), 5),
                ("BOTTOMPADDING", (1, -1), (1, -1), 10),
                ("RIGHTPADDING", (1,0), (1,-1), 13),
                ("BOTTOMPADDING", (1, -1), (1, -1), 10),
            ],
        )

        t.wrapOn(self.canv, self.width, self.height)
        t.drawOn(self.canv, *self.coord(self.x, 0, mm))
