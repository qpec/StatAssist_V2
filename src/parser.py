"""This should be the main pdf reader module, it reads the pdf
and returns a dictionary with all words, their respective
coordinates, and the page their on."""

from src.Config import highlight_margin
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
import re
import sys

def cord_evaluator(coordinate_list, highlight_margin=highlight_margin):
    # Coordinates are: x1, y1, x2, y2
    y_deviation = False
    if len(coordinate_list) > 1:
        x1 = []
        x2 = []
        y1 = []
        y2 = []
        for cords in coordinate_list:
            x1.append(cords[0] - highlight_margin)
            x2.append(cords[2] + highlight_margin)
            y1.append(cords[1] - highlight_margin)
            y2.append(cords[3] + highlight_margin)
        if y1[0] != y1[-1]:
            y_deviation = True
        if y_deviation:
            # here can insert function that evaluates initial
            # two words or more that are on the same line
            return coordinate_list[0]
        else:
            new_cords = (min(x1), min(y1), max(x2), max(y2))
            return new_cords
    else:
        return coordinate_list[0]
# Explanation of analysis:
# 1. Read PDF File
# 2. For each page of PDF file
# 3. Find LTTextBox fields
# 4. Find words inside LTTextBox
# 5. Calculate word coordinates by finding first and last letter  boxes
def analysis(pdf_file_path):
    try:
        f = open(pdf_file_path, "rb")
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

    except Exception as e:
        print("Error opening pdf file", e)
        sys.exit(1)

    print("Starting word analysis...")
    words = []
    coordinates = []
    pages = []

    for idx, page in enumerate(PDFPage.create_pages(doc)):
        interpreter.process_page(page)
        layout = device.get_result()
        for x in layout:
            if (
                type(x).__name__ == "LTTextBoxHorizontal"
                or type(x).__name__ == "LTTextBoxVertical"
            ):
                for y in x:
                    text = y.get_text()
                    word = ""
                    # Coordinates are: x1, y1, x2, y2
                    # Which make a rectangular selection to highlight the text
                    cords = []
                    for z in y:  # for each letter
                        if z.get_text().isalpha():
                            word += z.get_text()
                            try:
                                cords.append(z.bbox)
                            except:
                                continue
                        else:
                            if word != "":
                                words.append(word)
                                pages.append(idx)
                                # TODO fix only last letter highlighting
                                coordinates.append(cord_evaluator(cords))
                                word = ""
                                cords = []

    print("Word analysis completed...")
    f.close()
    return {
        "words": words,
        "pages": pages,
        "coordinates": coordinates,
        "total_pages": idx,
    }
