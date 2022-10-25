import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
from itertools import islice
import csv
import os
import glob
import pdftotext
import pandas as pd

def titlecase(s):
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda word: word.group(0).capitalize(),
        s)

os.chdir('/Users/miguelgarcia/Desktop/Work/LitigationTracking/September-October/complaints-20221004-MiguelRun/Cut/')

df1 = pd.read_csv('MiguelAugustRun.csv')

delimiter_dict = ['Company', 'INCORPORATED', 'Inc.', 'L.P.', 'LP', 'LLC', 'L.L.C.', 'Corporation', 'Co.', \
                  'Ltd', 'PLC', 'PBC', 'P.C.', 'L.L.C', 'S.A.', 'U.S.A.', 'USA', 'Inc']

def_list = []
write_list = []


row_num = len(df1.index)

for i in range(0, row_num):
    def_row = df1.iloc[i][4], df1.iloc[i][0], df1.iloc[i][3], df1.iloc[i][5], df1.iloc[i][6]
    def_list.append(def_row)

for defendant in def_list:
    input_case_id = defendant[0]
    input_def_name = defendant[1]
    input_docket_name = defendant[2]
    input_def_order = defendant[3]
    input_complaint_order = defendant[4]

    output_case_id = input_case_id
    output_def_name = titlecase(input_def_name)
    output_docket_name = input_docket_name
    output_def_order = input_def_order
    output_complaint_order = input_complaint_order

    #for delimeter in delimiter_dict:
    #    re.search(delimeter, output_def_name, flags=re.IGNORECASE)

    output_def_row = output_case_id, output_def_name, output_docket_name, output_def_order, output_complaint_order

    write_list.append(output_def_row)
    print(output_def_row)



with open('output_titlecase_defendantSTEPEHENPFAS082022.csv', 'w', newline='', encoding='utf-8') as result_file:
    wr = csv.writer(result_file)  # , dialect='excel')
    for i in write_list:
        wr.writerows([i])

