import PyPDF2
import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
from itertools import islice
import csv

file = open("0001577 - City of Oconomowoc Wasterwater Tre.pdf", "rb")
reader = PdfFileReader(file)

page1 = reader.getPage(0)
#print(page1)

page1Data = page1.extractText()
list = [page1Data]
#print(page1Data)
print(list)

vs_test_dict = ['vs\.', 'against', 'v\.'] #need the '\' or else 'v.' matches up to 'vi' Why?

delimiter_dict = ['Company', 'INCORPORATED', 'Inc.', 'L.P.', 'LP', 'LLC', 'L.L.C.', 'Corporation', 'Co.']

fka_dict = ['f/k/a', 'fka', 'd/b/a', 'dba']

successor_dict = ['individu', 'successo'] #for 'individually and as successor', 'successor-in-interest'



present_vs = None
flag_vs = None

text = None


for vs in vs_test_dict:
    pattern = "rB'" + vs + "'" # need to 'B' to make sure the string ends in the above in vs_dict
    print(pattern)
    search_string = re.compile(pattern)
    present_vs = re.search(vs, page1Data)
    print(present_vs, " is present")

    if present_vs:
        flag_vs = vs.replace('\\', '')
        text = page1Data.split(flag_vs)[1]
        text = text.split('Defendants.')[0]
        #print('names: ', text)

        break #will get info when it matches and dip

#print('names are: ', text)
print('after break')

list = [text.replace('\n', '')]
print(list)
text = text.join(list)
#print(text)

comma_indexes = [x.start() for x in re.finditer(',', text)]
print(comma_indexes)  # <-- [6, 13, 19]


sentence_list = []
defendants = []
#defendant_count = len(sentence_list)
#print(defendant_count)

#Will eeminate Commas from list of defendants if semi-colons are not present
#will distingiush between companies with US., Inc. names
#will also keep names if FKA / DBA is present
start_index = 0
for comma in comma_indexes[:]:
    end_index = comma
    curr_index = comma_indexes[:].index(comma)

    if start_index==end_index: #needed for if we remove a comma, and will need to skip the index
        continue

    search_end = end_index + 10  # checks for 'f/k/a' and /d/b/a' or '(f/k/a)', etc->'3M fka Minnesota'
    search_area = text[end_index:search_end]
    #if '\\n' in search_area:
        #search_area.

    print('search area includes: ', search_area)

    #needs to +1 bc we are not starting index at comma (index 0, and every other variable will)
    next_comma_text = text[end_index:]
    #next_comma = re.search(r"[^,]*,[^,]*", next_comma_text)

    next_comma = None
    try:
        next_comma = comma_indexes[curr_index + 1]
    except IndexError:
        next_comma = 'null'
    #next_comma = comma_indexes[curr_index + 1]
    #area_between_index = text[next_comma]

    name_in_question = text[start_index:end_index]
    print('name in question: ', name_in_question)

    break_loop_flag = False
    for fka in fka_dict:
        for delimeter in delimiter_dict:
            if text[end_index] == ',' and (fka.casefold() in search_area.casefold() or delimeter.casefold() in search_area.casefold()):
                print(text[start_index:end_index])
                print("yes there is a comma at index: ", end_index, ' and other name in search area: ', search_area)
                end_index = next_comma
                search_end = end_index + 10
                search_area = text[end_index:search_end]
                comma_indexes.remove(comma)
                # re.finditer(','[end_flag_index])
                # name = text.lstrip().replace('\n', '').split(',')[0]
                # print('name is: ', name)
                break_loop_flag = True
                break
            else:
                continue
        # leaves loop to speed up check process(if found)
        if break_loop_flag == True:
            break
        else:
            continue



            #comma++
        #out of delimeter dict
        #break

            # text = text.split('Defendants.')[0]
            # print(text)
    # out of FKA for loop
    so_far = text[start_index:end_index]
    print('names so far: ', text[start_index:end_index])


    for successor in successor_dict:
        if successor.casefold() in search_area.casefold():
            end_index = next_comma
            search_end = end_index + 10
            search_area = text[end_index:search_end]
            #comma_indexes.remove(comma)
            break_loop_flag = True
            break
        # leaves loop to speed up check process(if found)
    if break_loop_flag == True:
        continue
            


    pish = text[:end_index]
    posh = text[end_index + 1:]

    text = text[:end_index] + ';' + text[end_index + 1:]
    start_index = end_index

print(text)
print(comma_indexes)

#removes commas from comma_indexes for 'successor' companies
start_index = 0
#copy of edited comma_indexes
for comma in comma_indexes[:]:
    end_index = comma
    curr_index = comma_indexes[:].index(comma)

    if start_index==end_index: #needed for if we remove a comma, and will need to skip the index
        continue

    search_end = end_index + 10  # checks for 'f/k/a' and /d/b/a' or '(f/k/a)', etc->'3M fka Minnesota'
    search_area = text[end_index:search_end]
    #if '\\n' in search_area:
        #search_area.

    #print('search area includes: ', search_area)

    #needs to +1 bc we are not starting index at comma (index 0, and every other variable will)
    next_comma_text = text[end_index:]
    #next_comma = re.search(r"[^,]*,[^,]*", next_comma_text)

    next_comma = None
    try:
        next_comma = comma_indexes[curr_index + 1]
    except IndexError:
        next_comma = 'null'


    for successor in successor_dict:
        if text[end_index] == ',' and successor.casefold() in search_area.casefold():
            end_index = next_comma
            search_end = end_index + 10
            search_area = text[end_index:search_end]
            comma_indexes.remove(comma)
            break



    pish = text[:end_index]
    posh = text[end_index + 1:]

    text = text[:end_index] + ';' + text[end_index + 1:]
    start_index = end_index


#replaces useful commas with semi-colons, to help
for comma in comma_indexes:
    text = text[:comma] + ';' + text[comma + 1:]
text = text.lstrip()
print(text)
defendants = re.split(';', text)

print(defendants)

with open('test2_v2File.csv', 'w+', newline='') as result_file:
    # for item in list_of_Defendants:
    # result_file.write('%s\n' % item)

    wr = csv.writer(result_file)  # , dialect='excel')
    #wr.writerows([[defendants]])

    for i in defendants:
        wr.writerows([[i]])

'''
https://stackoverflow.com/questions/39112491/how-to-write-list-to-csv-with-each-item-on-a-new-row
'''


