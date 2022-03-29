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
#print(list)

vs_test_dict = ['vs\.', 'against', 'v\.'] #need the '\' or else 'v.' matches up to 'vi' Why?

delimiter_dict = ['Company', 'INCORPORATED', 'Inc\.', 'L\.P\.', 'LP', 'LLC', 'L\.L\.C\.', 'Corporation', 'Co\.']

fka_dict = ['f/k/a', 'fka', 'd/b/a', 'dba']

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

comma_indexes = [x.start() for x in re.finditer(',', text)]
print(comma_indexes)  # <-- [6, 13, 19]

sentence_list = []
defendants = []
#defendant_count = len(sentence_list)
#print(defendant_count)

print('now in separator\n')
for separator in delimiter_dict:
    pattern = "rB'" + separator + "'"  # need to 'B' to make sure the string ends in the above in vs_dict
    print('pattern is: ', pattern)
    search_string = re.compile(pattern)
    present_vs = re.search(separator, text, flags=re.IGNORECASE)
    print(present_vs, " is present")

    if present_vs:
        separator_comma = separator + ','
        print('comma separator: ', separator_comma)

        while present_vs:
            flag_vs = separator.replace('\\', '')
            print("flag is: ", flag_vs)
            #delete ',' that goes after the separator/delimeter

            start_flag_index = re.search(flag_vs, text, flags=re.IGNORECASE).start() #should be a ','
            end_flag_index = re.search(flag_vs, text, flags=re.IGNORECASE).end() #should be a ','
            print(flag_vs, 'ends at ', end_flag_index)

            comma_check = text[end_flag_index]
            print('comma index: ', comma_check)

            print('text[comma check] :' ,text[start_flag_index:end_flag_index])
            print('text is: ', type(text))
            #sentence_list = [text.split()[comma_check]]

            # result = page1Data.split(separator)
            # defendant_count = len(sentence_list)

            #text.split()[comma_check]
            #print(text)
            print('list: ', sentence_list)

            search_end = end_flag_index + 10 #checks for 'f/k/a' and /d/b/a' or '(f/k/a)', etc->'3M fka Minnesota'
            search_area = text[end_flag_index:search_end]
            print('search area includes: ', search_area)

            second_comma = "r'" + '[^,]*,[^,]*' +  "'"
            #"r'" + '^(?:.*?(,)){1}' + "'"
            #[^,]*,[^,]*
            #'(.*?matchdate){2}', s, re.DOTALL
            print('second comma: ', re.search(r"[^,]*,[^,]*", text))
            next_comma = re.search(r"[^,]*,[^,]*", text).end()
            print('at index: ', next_comma, 'there is: ', text[next_comma])

            for fka in fka_dict:
                    while text[end_flag_index] == ',' and fka in search_area:
                        print(text[start_flag_index:end_flag_index])
                        print("yes there is a comma at index: ", end_flag_index, ' and other name in search area: ', search_area)
                        end_flag_index = next_comma
                        search_end = end_flag_index + 10
                        search_area = text[end_flag_index:search_end]
                        #re.finditer(','[end_flag_index])
                        #name = text.lstrip().replace('\n', '').split(',')[0]
                        #print('name is: ', name)
                    break
                    #text = text.split('Defendants.')[0]
                    #print(text)
            #out of FKA for loop

            text = text[:end_flag_index] + ';' + text[end_flag_index + 1:]

            present_vs = False



    #sentence_list = [sentence.lstrip().replace('\n', '') for sentence in re.split(separator, text, flags=re.IGNORECASE)]
    #result = page1Data.split(separator)
    #defendant_count = len(sentence_list)
    #print(defendant_count)
    #print(result)


print(sentence_list)

with open('defendants_test.csv', 'w+', newline='') as defendants_test_file:
    # for item in list_of_Defendants:
    # result_file.write('%s\n' % item)

    wr = csv.writer(defendants_test_file)  # , dialect='excel')
    wr.writerows([sentence_list])
