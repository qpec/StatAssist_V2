'''This should be the main pdf reader module, it reads the pdf
and returns a dictionary with all words, their respective
coordinates, and the page their on.'''

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
import re
import sys


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
            if (type(x).__name__ == "LTTextBoxHorizontal" or
                    type(x).__name__ == "LTTextBoxVertical"):
                for y in x:
                    text = y.get_text()
                    word = ""
                    # Coordinates are: x1, y1, x2, y2
                    # Which make a rectangular selection to highlight the text
                    cords = []
                    for z in y:	 # for each letter
                        if re.match('[A-Za-z]', (z.get_text())):
                            word += z.get_text()
                            try:
                                cords.append(z.bbox)
                            except:
                                continue
                        else:
                            if (word != ""):
                                words.append(word)
                                pages.append(idx)
                                # TODO fix only last letter highlighting
                                coordinates.append(cords[-1])
                                word = ""

    print("Word analysis completed...")
    f.close()
    return {"words": words, "pages": pages, "coordinates": coordinates,
            "total_pages": idx}
