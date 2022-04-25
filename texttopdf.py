import PyPDF2
import pdftotext
import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
from itertools import islice
import csv
import os
#import cv
import numpy as np
from io import open
from fpdf import FPDF

# save FPDF() class into
# a variable pdf
pdf = FPDF()

# Add a page
pdf.add_page()

# set style and size of font
# that you want in the pdf

pdf.set_font("Times", size=11)

# open the text file in read mode
fd = open("Practices/C880_1edit.txt", "r", encoding="utf-8")
#pdf.set_doc_option('core_fonts_encoding', 'utf-8')
#fd = open("C880_1edit.txt", "r")

text = ''
with open('Practices/C880_1edit.txt') as f:
    lines = f.readlines()

text = text.join(lines)
text2 = text.encode()

#utxt = unicode(fd, 'utf-8')


#stxt = utxt.encode('iso-8859-1')


#u = fd.encode('iso-8859-1')
#print(fd)



#print(u)

# insert the texts in pdf
for i in fd:
    pdf.cell(200, 10, txt=i, ln=1, align='L')

#save the pdf with name .pdf
pdf.output("mygfg.pdf")
