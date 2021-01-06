from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
import csv
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
from collections import OrderedDict
import csv
from itertools import groupby
import itertools
import urllib
import webbrowser
import os
import glob

roll = int(input("Roll: "))
list_of_files_with_rolls = []

for path, dirs, files in os.walk("...2018"):
    for d in dirs:
        for f in glob.iglob(os.path.join(path, d, '*.pdf')):
            # print(f)
            list_of_files_with_rolls.append(f)


for i in list_of_files_with_rolls:
    if "LUC" in i and str(roll) in i:
        roll_LUC = i
        break
    if "assessment" in i and str(roll) in i:
        roll_LUC = i
        break
    if str(roll) in i:
        roll_LUC = i

data = []


def parse_layout(layout):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:

        # print(lt_obj.bbox)
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            print(lt_obj.get_text())
            data.append([lt_obj.bbox[3], lt_obj.get_text().splitlines()])
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj)  # Recursive

try:
    fp = open(roll_LUC, 'rb')

    parser = PDFParser(fp)
    doc = PDFDocument(parser)

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        parse_layout(layout)

except NameError:
    print("No LUC found")