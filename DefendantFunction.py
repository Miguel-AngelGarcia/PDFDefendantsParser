import pandas as pd
import glob
import numpy as np
import os
import csv
import re

def non_mdl_split(defendant_split, def_num):
    for function_defendant in defendant_split:
        split_list = []

    #to standardize names
        for i in range(0, def_num):
            fun_current = defendant_split[i]
            fun_current = fun_current.split('(')[0]
            fun_current = fun_current.replace('.', '').replace(',', '')
            fun_current = fun_current.lstrip().rstrip()

            #case_defendant_output.append()



os.chdir('/Users/miguelgarcia/Desktop/Work/LitigationTracking/Talc/')
case_defendant = pd.read_csv('talc_mdl_bloomberg_join2.csv')
print(case_defendant)

case_defendant = case_defendant.dropna(subset=['MDLDocketNumber'])
print(case_defendant)

row_num = len(case_defendant.index)

headers = 'DocketNumber', 'DefendantName', 'PotentialOtherName', 'Year'
header_flag = False

for i in range(0, row_num):

    case_defendant_output = []

    if header_flag == False:
        case_defendant_output.append(headers)
        header_flag = True

    case = case_defendant.iloc[i][10]

    year = case_defendant.iloc[i][11]
    year = year[-2:]
    year = '20' + year

    defendant_row_string = case_defendant.iloc[i][14]

    defendant_split = defendant_row_string.split('/')
    def_num = len(defendant_split)


    for x in range(0, def_num):
        rough = defendant_split[x]
        qmi_flag = False
        other_name = ''

        current_defendant = rough
        current_defendant = current_defendant.split('(')[0]
        current_defendant = current_defendant.lstrip().rstrip()

        quotation_marks_indices = [x.start() for x in re.finditer('"', rough)]
        if quotation_marks_indices:
            qmi_flag = True

        if qmi_flag == True:
            quote_start = quotation_marks_indices[0] + 1
            quote_end = quotation_marks_indices[-1]
            other_name = rough[quote_start:quote_end]


        input = case, current_defendant, other_name, year

        case_defendant_output.append(input)

    with open('CaseDefendant.csv', 'a+', newline='', encoding='utf-8') as result_file:
        wr = csv.writer(result_file)  # , dialect='excel')
        # for row in open("test2_v2File.csv"):
        # row_count += 1
        # print('row count: ', row_count)
        for i in case_defendant_output:
            wr.writerows([i])



