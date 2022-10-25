import pandas as pd
import os
from decimal import Decimal
import csv
import re

def output_file_writer(write_list):
    with open('CasesCompletedDefendants.csv', 'a+', newline='', encoding='utf-8') as result_file:
        wr = csv.writer(result_file)  # , dialect='excel')
        # for row in open("test2_v2File.csv"):
        # row_count += 1
        # print('row count: ', row_count)
        for i in write_list:
            wr.writerows([i])



os.chdir('/Users/miguelgarcia/PycharmProjects/PDF/')

completed = pd.read_csv('CasesDone.csv')
list_of_complaints = pd.read_csv('filenames.csv')


row_num_work = len(completed.index)
row_num_lowes = len(list_of_complaints.index)

completed_info = []
list_info = []

ignore_dict = ['NoNamePoss', 'NoNameGrabbed']

'''
1.) string to string match, case-insensitive
2.) string to string match, removing ',' and '.' | ie-> L.L.C. vs LLC
3.) string to string match, comparing Inc to incorporated, corp to corporation, etc. 
4.) remove company ending (ie. corp, inc, PLC, etc), then do string-to-string
'''

# Gets info from db_file
for i in range(0, row_num_work):
    #                    FileName
    completed_row = completed.iloc[i][0]

    edited_filename = completed_row.replace("after", "")
    edited_filename = edited_filename.replace("pdf", "PDF")

    completed_input_row = edited_filename
    print(completed_input_row)

    completed_info.append(completed_input_row)

#gets info from lowes file
for i in range(0, row_num_lowes):
    #                       PotentiaName   |         CASno
    list_input_row = list_of_complaints.iloc[i][0]

    print(list_input_row)
    list_info.append(list_input_row)

first_row_present = False

for list_candidate in list_info:
    write_list = []

    if first_row_present == False:
        first_row_present = True
        first_row = 'Filename', 'Status'
        write_list.append(first_row)

    file_match = False

    for completed in completed_info:
        match = completed == list_candidate

        if match:
            file_match = True
            matched_row = list_candidate, 'Completed'

            # insets into write list
            write_list.append(matched_row)

            # removed row lessen list / speed maybe?
            list_info.remove(list_candidate)

            print(matched_row)
            output_file_writer(write_list)

            # gets out and should go to lowes_db_CAS_match statement below
            break

    if file_match == False:
        unmatched_file = list_candidate, 'Not Completed'
        write_list.append(unmatched_file)

        print(unmatched_file)
        output_file_writer(write_list)



