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

file = open("C1_1.pdf", "rb")

dict = "vs."

reader = PdfFileReader(file)

page1 = reader.getPage(0)
#print(page1)

page1Data = page1.extractText()
#print(page1Data)

with Path('defendants_names.txt').open(mode='w') as output_file1:
    text = ''
    for page in reader.pages:
        text += page.extractText()
    output_file1.write(text)

# Get number of pages
NumPages = reader.getNumPages()

# Enter code here
vs = "vs."
defendants = "Defendants."

vsPage = 0
defendantsPage = 1

# Extract text and do the search
for i in range(0, NumPages):
    PageObj1 = reader.getPage(i)
    Text1 = PageObj1.extractText()
    if re.search(vs, Text1):
        print("'vs.' Found on Page: " + str(i))
        vsPage = str(i)

for i in range(0, NumPages):
    PageObj2 = reader.getPage(i)
    Text2 = PageObj2.extractText()
    if re.search(defendants, Text2):
        print("'Defendants.' Found on Page: " + str(i))
        defendantsPage = str(i)
        if vsPage == defendantsPage:
            print("we got a match")

            split = re.split('vs.', Text2)
            # print(split)

            break
        else:
            print("no match")

vsPageInt = int(vsPage)
defendantsPageInt = int(defendantsPage) + 1
defendantPages = []
"""
for page in reader.pages:
    page_num = page['/StructParents']
    page_text = page.extractText()
    print('vs. @:' + str(vsPageInt) + 'defendant. @:' + str(defendantsPageInt))

    for i in range(vsPageInt, defendantsPageInt):
        defendantPages.append(page_num)
"""

print(NumPages, vsPageInt, defendantsPageInt)
for page in islice(range(NumPages), vsPageInt, defendantsPageInt):
    print("startig")
    page_num = reader.getPage(i)
    print(page_num)
    print("this is # " + str(i))
    page_text = page_num.extractText()
    print('vs. @:' + str(vsPageInt) + 'defendant. @:' + str(defendantsPageInt))
    defendantPages.append(i)

    """
    page_num = page['/StructParents']
    page_text = page.extractText()

    defendantPages.appeand(page_num)
    """

print(defendantPages)

# create fileWriter object
pdf_writer = PdfFileWriter()

for page in defendantPages:
    page_object = reader.getPage(page)
    pdf_writer.addPage(page_object)

# save pages as pdf
with Path('defendants_names.pdf').open(mode='wb') as output_file2:
    pdf_writer.write(output_file2)

# going to pull defendant from pages

filename = "defendant.csv"
f = open(filename, "w")

headers = "ListedName, F/K/A, D/B/A\n"
f.write(headers)

list_of_Defendants = []

for page in islice(range(NumPages), vsPageInt, defendantsPageInt):
    page_num = reader.getPage(i)
    page_text = page_num.extractText()
    print('hi')

    #print(page_text)

    take2 = [page_text]
    print("take 2: ", take2)

    #sentence_list = [sentence for sentence in re.split('\n', page_text)]
    #print(sentence_list)

    # test = "'1\n \n \nUNITED STATES DISTRICT COURT\n \nDISTRICT OF \nMASSACHUSETTS\n \nWORCESTER\n \nDIVISION\n \n \nThomas BURKE\n; Randi BURKE;\n \n \n \n \nJoshua CHACKO; Asha CHACKO; Federico \nRAFFA; Melisa CUNNINGHAM;  Ryan \nDORTCH; Melanie DORTCH; \nSuzanne HAYS; \nFred\nerick\n \nHAYS\n, JR.\n; \nLawrence \nHETTINGER; \nEdie HUBER; Brian KING; Julia KING;\n \nSean \nMURPHY; Kimberley MURPHY; Christopher \nKRUEGLER; and\n \nGillian PRICE, \n \n \n \nPlaintiff\ns,\n \n \nvs.\n \n \n3M\n \nCOMPANY\n \n(f/k/a\n \nMinnesota\n \nMining\n \nand\n \nManufacturing,\n \nCo.);\n \nAGC, INC. (f/k/a Asahi \nGlass Co.,\n \nLtd.);\n \nAGC\n \nCHEMICAL\n \nAMERICAS,\n \nINC.;\n \nARCHROMA \nMANAGEMENT, LLC; ARCHROMA\n \nU.S.,\n \nINC.; ARKEMA,\n \nINC.;\n \nBASF\n \nCORPORATION; BUCKEYE\n \nFIRE\n \nEQUIPMENT\n \nCOMPANY; CARRIER\n \nGLOBAL\n \nCORPORATION; CHEMDESIGN\n \nPRODUCTS,\n \nINC.; CHEMGUARD,\n \nINC.; \nCHEMICAL COMPANY; \nCHEMICALS\n \nINCORPORATED; THE\n \nCH\nEMOURS\n \nCOMPANY;\n \nTHE\n \nCHEMOURS\n \nCOMPANY\n \nFC,\n \nLLC; CHUBB\n \nFIRE, LTD.; CLARIANT\n \nCORPORATION;\n \nCORTEVA,\n \nINC.; \nDEEPWATER \nCHEMICALS, INC.; DUPONT\n \nDE\n \nNEMOURS,\n \nINC.; DYNAX\n \nCORPORATION; E. I. DU PONT DE \nNEMOURS AND\n \nCOMPANY; KIDDE\n \nPLC,\n \nINC.;\n \nKIDDE\n-\n \nFENWAL,\n \nINC.;\n  \nNATIONAL\n \nFOAM,\n \nINC.;\n  \nNATION\n \nFORD; RAYTHEON   \n \nTECHNOLOGIES CORPORATION\n \n(f/k/a\n \nUnited\n \nTechnologies\n \nCorporation);\n \nTYCO\n \nFIRE\n \nPRODUCTS\n \nLP\n \n(successor\n-\nin\n-\ninterest\n \nto\n \nThe\n \nAnsul\n \nCompany);\n \nand\n \nUTC\n \nFIRE\n \n&\n \nSECURITY\n \nAMERICAS\n \nCORPORATION,\n \nINC.\n, \n \n \n \n \n \n', '\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n)\n \n \n \nCivil Case No.:\n  \n \n \nCOMPLAINT\n \nAND JURY DEMAND\n \n \n \n \nCase 4:21-cv-40137   Document 1   Filed 12/29/21   Page 1 of 31'"

    # result = re.match('(?<=vs.)(.*)(?=Defendants.)',sentence_list).group()
    # print(result)

    pattern = '^(.*)(?=vs.)'
    patt2 = '^(.*vs.)'
    patter3 = re.compile(r'vs.')
    new_page_text = re.sub(patter3, "", page_text)
    #print(new_page_text)
    #print(new_page_text)
    print(type(page_text))

    print('next thing')
    test3 = page_text.split('vs.')[-1]
    test3 = test3.split('Defendants.')[0]
    print(test3)

    sentence_list = [sentence.lstrip().replace('\n', '') for sentence in re.split(';', test3)]
    defendant_count = len(sentence_list)
    print(defendant_count)

    index_def_count = defendant_count - 1

    potential_and = sentence_list[index_def_count]
    print(potential_and)

    if 'and' in potential_and:
        potential_and = potential_and.replace("and", "").lstrip().rstrip().rstrip(',')
        print(potential_and)
        print(type(potential_and))
        sentence_list[index_def_count] = potential_and

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

        if re.search('f/k/a', line):  # do some regex magiv for fka, f/k/a, FKA, F/K/A, etc
            print("yes, there is fka'")
            # x = len(re.search('f/k/a'))
            element1 = line.split(r'(')[0].lstrip()
            element2 = line.split('f/k/a', 1)[-1].rstrip(')').lstrip()
            print('element 1: ', element1)
            print('element 2: ', element2)


        else:
            print("nope, no fka")

        if re.search('d/b/a', line):
            print("yes, there is dba'")
            element1 = line.split(r'(', 1)[0].lstrip()
            element3 = line.split('d/b/a', 1)[-1].rstrip(')').lstrip()

        else:
            print("nope, no dba")

        with open('output.csv', 'w+', newline='') as result_file:
            for item in sentence_list:
                result_file.write('%s\n' % item)

        next_defendant = [element1, element2, element3]
        list_of_Defendants.append(next_defendant)

    print(sentence_list)

    print(list_of_Defendants)
    # list_of_Defendants = [list_of_Defendants for defendants][0]
    print((list_of_Defendants))

    #    for item in sentence_list:
    #       result_file.write('%s\n' % item)

    with open('output.csv', 'w+', newline='') as result_file:
        # for item in list_of_Defendants:
        # result_file.write('%s\n' % item)

        wr = csv.writer(result_file)  # , dialect='excel')
        wr.writerows(list_of_Defendants)

    """
    #split word is String
    defendants =  reader.partition(String)
    print("ok, here they are: ")
    print(defendants)
    """

    # result = re.search('vs.(.*)Defendants.',reader)
    # pattern = (?<=vs.).*(?=Defendants.)


