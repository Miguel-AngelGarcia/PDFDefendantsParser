import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
from itertools import islice
import csv

vs_dict = ['vs.', 'v.', 'against']
fka_dict = ['f/k/a', 'fka']

string = 'Mark against Joe'

def name_remover(fka, name):
    print(fka,' found, removing ', name,  ' from list')
    names.remove(name)
    print('names in list: ', names)
    print('')

for vs in vs_dict:
    print('Current word: ', vs)
    if re.search(vs, string):
        print('found')
        new = re.split(vs, string)[-1]
        print('new string: ', new)

    else:
        print('not found')

print('')

names = ['3M COMPANY (f/k/a Minnesota Mining and Manufacturing, Co.)', 'AGC, INC. (f/k/a Asahi Glass Co., Ltd.)', 'AGC CHEMICAL AMERICAS, INC.', 'ARCHROMA MANAGEMENT, LLC', 'ARCHROMA U.S., INC.', 'ARKEMA, INC.', 'BASF CORPORATION', 'BUCKEYE FIRE EQUIPMENT COMPANY', 'CARRIER GLOBAL CORPORATION', 'CHEMDESIGN PRODUCTS, INC.', 'CHEMGUARD, INC.', 'CHEMICAL COMPANY', 'CHEMICALS INCORPORATED', 'THE CHEMOURS COMPANY', 'THE CHEMOURS COMPANY FC, LLC', 'CHUBB FIRE, LTD.', 'CLARIANT CORPORATION', 'CORTEVA, INC.', 'DEEPWATER CHEMICALS, INC.', 'DUPONT DE NEMOURS, INC.', 'DYNAX CORPORATION', 'E. I. DU PONT DE NEMOURS AND COMPANY', 'KIDDE PLC, INC.', 'KIDDE- FENWAL, INC.', 'NATIONAL FOAM, INC.', 'NATION FORD', 'RAYTHEON    TECHNOLOGIES CORPORATION (f/k/a United Technologies Corporation)', 'TYCO FIRE PRODUCTS LP (successor-in-interest to The Ansul Company)', 'UTC FIRE & SECURITY AMERICAS CORPORATION, INC.']

print('names in list: ', names)

for fka in fka_dict:
    print('fka word: ', fka)

    for name in names[:]: #this colon iterates through a copy of the list
                          #Prevents skipping/cannot remove items while iterating
                          #will removing from names[] list
                          #But, will be going over all names because they remain unchanged in the copy of the list
        print('current name: ', name)
        if re.search(fka, name):
            done = False

            print('found ', fka)

            fka_start_index = re.search(fka, name, flags=re.IGNORECASE).start()
            print(fka, 'start index: ', fka_start_index)

            parenthesis_check = fka_start_index - 1
            print('parenthesis index: ', parenthesis_check)

            if name[parenthesis_check] == '(':
                print('yes parenthesis')

                first_name = name.split('(', 1)[0]
                print('first name: ', first_name)

                pattern = '(' + fka
                print('pattern :', pattern)
                second_name = name.split(pattern, 1)[-1].lstrip().rstrip(')')
                print('second name: ', second_name)

                done = True


            else:
                print('no parenthesis')
                second_name = name.split(fka)[0]
                print('first name: ', second_name)

                second_name = name.split(fka)[-1].lstrip()
                print('second name: ', second_name)
                #new = name.split(fka, name)
                #element1 = line.split(r'f/k', 1)[0].lstrip()  # 'f/k/a' for f/ or '(' for (f/k/a
                #element2 = line.split('f/k/a', 1)[-1].rstrip(')').lstrip()
                print('new string')

                done = True

            #name = name -1
            if done:
                name_remover(fka, name)


            print('')

        else:
            print('did not find ', fka)


print(names)