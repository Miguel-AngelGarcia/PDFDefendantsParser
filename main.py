# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
"""
WRITE A FUNCTION FOR BETTER USE NEXT TIME
def fnPDF_FindText(xFile, xString):
    # xfile : the PDF file in which to look
    # xString : the string to look for
    import pyPdf, re
    PageFound = -1
    pdfDoc = pyPdf.PdfFileReader(file(xFile, "rb"))
    for i in range(0, pdfDoc.getNumPages()):
        content = ""
        content += pdfDoc.getPage(i).extractText() + "\n"
        content1 = content.encode('ascii', 'ignore').lower()
        ResSearch = re.search(xString, content1)
        if ResSearch is not None:
           PageFound = i
           break
     return PageFound
"""

"""
1.) count pages from 'vs.' to 'Defendants.'
    ie. Burke
    vs.
    3M; DuPont; etc
    Defendants.
    
    ->if it takes multiple pages to go from 'vs.' to 'Defendant.' then make sure to count them
    and throw them into a loop?
2.) extract all defendants


"""


import PyPDF2
import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
from itertools import islice
import csv

file = open("0001624 - Burke v. 3M Company.pdf", "rb")

dict = "vs."

reader = PdfFileReader(file)

#page1 = reader.getPage(0)
#print(page1)

#page1Data = page1.extractText()
#print(page1Data)

with Path('defendants_names.txt').open(mode = 'w') as output_file1:
    text = ''
    for page in reader.pages:
        text += page.extractText()
    output_file1.write(text)



# Get number of pages
NumPages = reader.getNumPages()

# Enter code here
vs = "against" #'vs.', 'v.', 'against'
defendants = "Defendants."

vsPage = 0
defendantsPage = 1


# Extract text and do the search
for i in range(0, NumPages):
    PageObj1 = reader.getPage(i)
    Text1 = PageObj1.extractText()
    if re.search(vs,Text1):
        print("'vs.' Found on Page: " + str(i))
        vsPage  = str(i)

    if re.search(defendants,Text1):
        print("'Defendants.' Found on Page: " + str(i))
        defendantsPage = str(i)
        if vsPage == defendantsPage:
            print("we got a match")

            split = re.split('vs.', Text1)
            # print(split)

            break
        else:
            print("no match")

#for i in range(0, NumPages):
#    PageObj2 = reader.getPage(i)
#    Text2 = PageObj2.extractText()
#    if re.search(defendants,Text2):
#        print("'Defendants.' Found on Page: " + str(i))
#        defendantsPage = str(i)
#        if vsPage == defendantsPage:
#           print("we got a match")
#
#
#            split = re.split('vs.', Text2)
#            #print(split)
#
#
#            break
#        else:
#            print("no match")

vsPageInt = int(vsPage)
defendantsPageInt = int(defendantsPage) + 1
defendantPages = []

print(NumPages, vsPageInt, defendantsPageInt)
for page in islice(range(NumPages), vsPageInt, defendantsPageInt):

    print("startig")
    page_num = reader.getPage(i)
    print(page_num)
    print("this is # " + str(i))
    page_text = page_num.extractText()
    print('vs. @:' + str(vsPageInt) + 'defendant. @:' + str(defendantsPageInt))
    defendantPages.append(i)

#print(defendantPages)

#create fileWriter object
pdf_writer = PdfFileWriter()

for page in defendantPages:
    page_object = reader.getPage(page)
    pdf_writer.addPage(page_object)

#save pages as pdf
with Path('defendants_names.pdf').open(mode = 'wb') as output_file2:
    pdf_writer.write(output_file2)

#going to pull defendant from pages

filename = "defendant.csv"
f = open(filename, "w")

headers = "ListedName, F/K/A, D/B/A\n"
f.write(headers)


list_of_Defendants = []

for page in islice(range(NumPages), vsPageInt, defendantsPageInt):
    page_num = reader.getPage(i)
    page_text = page_num.extractText()
    #print('hi')

    #print(page_text)

    take2 = [page_text]
    #print(take2)

    #sentence_list = [sentence for sentence in re.split('\n', page_text)]
    #print(sentence_list)


    print('next thing')
    test3 = page_text.split(vs)[-1]
    test3 = test3.split('Defendants.')[0]
    print(test3)


    sentence_list = [sentence.lstrip().replace('\n', '') for sentence in re.split('\.,', test3)] #';', '.,'
    defendant_count = len(sentence_list)
    print(defendant_count)

    index_def_count = defendant_count - 1

    potential_and = sentence_list[index_def_count]
    print(potential_and)

    if 'and' in potential_and:
        potential_and = potential_and.replace("and", "").lstrip().rstrip().rstrip(',')
        print(potential_and)
        print(type(potential_and))
        sentence_list[index_def_count]= potential_and

    for line in sentence_list:
        print("line: ", line)
        curr_index = sentence_list.index(line)
        print("current index: ", curr_index)
        print(sentence_list)
        list_element = sentence_list[curr_index]
        print('list element: ', list_element)

        element1 = line
        element2 = 'NULL'
        element3 = 'NULL'

        if re.search('f/k/a', line): #do some regex magiv for fka, f/k/a, FKA, F/K/A, etc
            print("yes, there is fka'")
            #x = len(re.search('f/k/a'))
            element1 = line.split(r'f/k', 1)[0].lstrip() #'f/k/a' for f/ or '(' for (f/k/a
            element2 = line.split('f/k/a', 1)[-1].rstrip(')').lstrip()

        else:
            print("nope")


        if re.search('d/b/a', line):
            print("yes, there is dba'")
            element1 = line.split(r'(', 1)[0].lstrip()
            element3 = line.split('d/b/a', 1)[-1].rstrip(')').lstrip()

        else:
            print("nope")

        #with open('output.csv', 'w+', newline='') as result_file:
         #   for item in sentence_list:
         #       result_file.write('%s\n' % item)

        next_defendant = [element1, element2, element3]
        list_of_Defendants.append(next_defendant)

    print(sentence_list)

    print(list_of_Defendants)
    #list_of_Defendants = [list_of_Defendants for defendants][0]
    print((list_of_Defendants))

        #    for item in sentence_list:
         #       result_file.write('%s\n' % item)

    with open('output2.csv', 'w+', newline='') as result_file:
        #for item in list_of_Defendants:
            #result_file.write('%s\n' % item)


        wr = csv.writer(result_file)#, dialect='excel')
        wr.writerows(list_of_Defendants)




    #result = re.search('vs.(.*)Defendants.',reader)
    #pattern = (?<=vs.).*(?=Defendants.)


