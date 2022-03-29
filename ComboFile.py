import PyPDF2
import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
from itertools import islice
import csv
import os

def name_remover(fka, defendant):
    print(fka,' found, removing ', defendant,  ' from list')
    defendant.remove(defendant)
    print('names in list: ', defendant)
    print('')

def semi_colon_checker(text):
    print('at checker')
    if ';' in text:
        print('yes it is')
        defendants = [defendant.lstrip().rstrip() for defendant in re.split(';', text)]
        global semi_colon_flag
        semi_colon_flag= True
        #return(semi_colon_flag)

def error_file_write(file):
    with open('test2_v2File.csv', 'a+', newline='') as result_file:
        wr = csv.writer(result_file)  # , dialect='excel')
        element1 = 'File'
        element2 = 'Not'
        element3 = 'Read'
        element4 = file
        list_of_Defendants = [element1, element2, element3, element4]
        for i in list_of_Defendants:
            wr.writerows([i])


path = "/Users/miguelgarcia/Desktop/Files"
dir_list = os.listdir(path)

print("Files and directories in '", path, "' :")
row_count = 0
#print the list
print(dir_list)
#file = open("0001624 - Burke v. 3M Company.pdf", "rb")

for file in dir_list:
    semi_colon_flag = False
    reader = None
    try:
        reader = PdfFileReader(file)
    except IOError:
        print("Could not read file: ", file)
        error_file_write(file)
        break

    print('reading file: ', file)

    page1 = reader.getPage(0)
    # print(page1)

    page1Data = page1.extractText()
    list = [page1Data]
    # print(page1Data)
    #print(list)

    vs_test_dict = ['vs\.', 'against', 'v\.']  # need the '\' or else 'v.' matches up to 'vi' Why?
    delimiter_dict = ['Company', 'INCORPORATED', 'Inc.', 'L.P.', 'LP', 'LLC', 'L.L.C.', 'Corporation', 'Co.', 'Ltd']
    fka_dict = ['f/k/a', 'fka', 'd/b/a', 'dba']
    successor_dict = ['individu', 'successo']  # for 'individually and as successor', 'successor-in-interest'

    present_vs = None
    flag_vs = None

    text = None

    for vs in vs_test_dict:
        pattern = "rB'" + vs + "'"  # need to 'B' to make sure the string ends in the above in vs_dict
        print(pattern)
        search_string = re.compile(pattern)
        present_vs = re.search(vs, page1Data)
        print(present_vs, " is present")

        if present_vs:
            flag_vs = vs.replace('\\', '')
            text = page1Data.split(flag_vs)[1]
            text = text.split('Defendants.')[0]
            # print('names: ', text)

            break  # will get info when it matches and dip

    # print('names are: ', text)
    print('after break')

    #turns text(STRING) into a list to remove '\n' and turns it back into a string
    list = [text.replace('\n', '')]
    #print(list)
    text = text.join(list)
    # print(text)

    comma_indexes = [x.start() for x in re.finditer(',', text)]
    #print(comma_indexes)  # <-- [6, 13, 19]

    sentence_list = []
    defendants = []
    # defendant_count = len(sentence_list)
    # print(defendant_count)

    # Will eeminate Commas from list of defendants if semi-colons are not present
    # will distingiush between companies with US., Inc. names
    # will also keep names if FKA / DBA is present
    text
    semi_colon_checker(text)


    #defendants = [sentence.lstrip().replace('\n', '') for sentence in re.split(';', text)]

    start_index = 0
    for comma in comma_indexes[:]:
        if semi_colon_flag == True:
            break

        end_index = comma
        curr_index = comma_indexes[:].index(comma)

        if start_index == end_index:  # needed for if we remove a comma, and will need to skip the index
            continue

        search_end = end_index + 10  # checks for 'f/k/a' and /d/b/a' or '(f/k/a)', etc->'3M fka Minnesota'
        search_area = text[end_index:search_end]
        # if '\\n' in search_area:
        # search_area.

        print('search area includes: ', search_area)

        # needs to +1 bc we are not starting index at comma (index 0, and every other variable will)
        next_comma_text = text[end_index:]
        # next_comma = re.search(r"[^,]*,[^,]*", next_comma_text)

        next_comma = None
        try:
            next_comma = comma_indexes[curr_index + 1]
        except IndexError:
            next_comma = 'null'
        # next_comma = comma_indexes[curr_index + 1]
        # area_between_index = text[next_comma]

        name_in_question = text[start_index:end_index]
        print('name in question: ', name_in_question)

        break_loop_flag = False
        for fka in fka_dict:
            for delimeter in delimiter_dict:
                if text[end_index] == ',' and (
                        fka.casefold() in search_area.casefold() or delimeter.casefold() in search_area.casefold()):
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

                # comma++
            # out of delimeter dict
            # break

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
                # comma_indexes.remove(comma)
                break_loop_flag = True
                break
            # leaves loop to speed up check process(if found)
        if break_loop_flag == True:
            continue

        pish = text[:end_index]
        posh = text[end_index + 1:]

        text = text[:end_index] + ';' + text[end_index + 1:]
        start_index = end_index

    #print(text)
    #print(comma_indexes)

    # removes commas from comma_indexes for 'successor' companies
    start_index = 0
    # copy of edited comma_indexes
    for comma in comma_indexes[:]:
        if semi_colon_flag == True:
            break

        end_index = comma
        curr_index = comma_indexes[:].index(comma)

        if start_index == end_index:  # needed for if we remove a comma, and will need to skip the index
            continue

        search_end = end_index + 10  # checks for 'f/k/a' and /d/b/a' or '(f/k/a)', etc->'3M fka Minnesota'
        search_area = text[end_index:search_end]
        # if '\\n' in search_area:
        # search_area.

        # print('search area includes: ', search_area)

        # needs to +1 bc we are not starting index at comma (index 0, and every other variable will)
        next_comma_text = text[end_index:]
        # next_comma = re.search(r"[^,]*,[^,]*", next_comma_text)

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

    # replaces useful commas with semi-colons, to help
    for comma in comma_indexes:
        if semi_colon_flag == True:
            break
        text = text[:comma] + ';' + text[comma + 1:]
    text = text.lstrip()
    #print(text)
    #defendants = re.split(';', text).lstrip()
    defendants = [defendant.lstrip().rstrip() for defendant in re.split(';', text)] #need to get rid of whitespace

    #print(defendants)

    defendant_count = len(defendants)
    #print(defendant_count)

    index_def_count = defendant_count - 1

    #elimanates any 'and's in the beginning of defendant names
    for defendant in defendants:
        curr_def_index = defendants.index(defendant)
        curr_def = defendants[curr_def_index]
        print(curr_def)

        and_pattern = re.compile("r'^and\s'")
        if re.match(r'^and\s', curr_def):
            print('yes it does')
            potential_and = curr_def.replace("and", "").lstrip()
            #print(potential_and)
        #    print(potential_and)
        #    print(type(potential_and))
            defendants[curr_def_index] = potential_and
            #print(curr_def)
    #print(defendants)

    #will separate defendants into fka/dba(s), successors,
    list_of_Defendants = []

    #writes names to file
    for defendant in defendants:
        print("defendant: ", defendant)
        curr_index = defendants.index(defendant)
        print("current index: ", curr_index)
        print(defendants)
        list_element = defendants[curr_index]
        print('list element: ', defendant)

        element1 = defendant
        element2 = 'NULL'
        element3 = 'NULL'
        element4 = file

        for fka in fka_dict:
            if re.search(fka, defendant):  # do some regex magiv for fka, f/k/a, FKA, F/K/A, etc
                # Prevents skipping/cannot remove items while iterating
                # will removing from names[] list
                # But, will be going over all names because they remain unchanged in the copy of the list
                done = False

                print('current name: ', defendant)
                print("yes, there is: ", fka)

                fka_start_index = re.search(fka, defendant, flags=re.IGNORECASE).start()
                print(fka, 'start index: ', fka_start_index)
                parenthesis_check = fka_start_index - 1
                print('parenthesis index: ', parenthesis_check)

                if defendant[parenthesis_check] == '(':
                    print('yes parenthesis')

                    comma_check = parenthesis_check - 1
                    if defendant[comma_check] == ',':
                        print('yes, there is a comma')
                        defendant = defendant[:comma_check] + defendant[comma_check + 1:]

                    first_name = defendant.split('(', 1)[0].rstrip()
                    print('first name: ', first_name)

                    pattern = '(' + fka
                    print('pattern :', pattern)
                    second_name = defendant.split(pattern, 1)[-1].lstrip().rstrip(')')
                    print('second name: ', second_name)

                    element1 = first_name
                    element2 = second_name

                    break

                else:
                    print('no parenthesis')

                    first_name = defendant.split(fka)[0].rstrip()
                    comma_check = len(first_name) - 1
                    print('comma at index: ', comma_check)

                    if defendant[comma_check] == ',':
                        print('yes, there is a comma')
                        first_name = defendant[:comma_check]

                    print('first name: ', first_name)

                    second_name = defendant.split(fka)[-1].lstrip()
                    print('second name: ', second_name)
                    #new = name.split(fka, name)
                    #element1 = line.split(r'f/k', 1)[0].lstrip()  # 'f/k/a' for f/ or '(' for (f/k/a
                    #element2 = line.split('f/k/a', 1)[-1].rstrip(')').lstrip()
                    print('new string')

                    element1 = first_name
                    element2 = second_name

                    break


                # x = len(re.search('f/k/a'))
                #element1 = defendant.split(r'(')[0].lstrip()
                #element2 = defendant.split(fka, 1)[-1].rstrip(')').lstrip()
                print('element 1: ', element1)
                print('element 2: ', element2)

                break

                print('found ', fka)




            else:
                print("nope, no: ", fka)

        for successor in successor_dict:
            if re.search(successor, defendant):
                successor_start_index = re.search(successor, defendant, flags=re.IGNORECASE).start()
                print('sucessor')
                print(defendant)
                parenthesis_check = successor_start_index - 1
                print('parenthesis index: ', parenthesis_check)
                print('check: ', defendant[successor_start_index])

                if defendant[parenthesis_check] == '(':
                    """
                    print('yes parenthesis')
                    defendant = defendant[:parenthesis_check] + defendant[parenthesis_check + 1:]
                    print('parenthesis one: ', defendant)
                    first_name = defendant.split(successor)[0].rstrip()

                    second_name = defendant.split(pattern, 1)[-1].lstrip().rstrip(')')
                    print('second name: ', second_name)
                    first_name = defendant.split(successor)[0].rstrip()
                    """

                    comma_check = parenthesis_check - 1
                    if defendant[comma_check] == ',':
                        print('yes, there is a comma')
                        defendant = defendant[:comma_check] + defendant[comma_check + 1:]

                    first_name = defendant.split('(', 1)[0].rstrip()
                    print('first name: ', first_name)

                    pattern = '('
                    print('pattern :', pattern)
                    successor_name = defendant.split(pattern, 1)[-1].lstrip().rstrip(')')
                    print('second name: ', second_name)

                    element1 = first_name
                    element3 = successor_name

                    break

                else:
                    print('no parenthesis')

                    first_name = defendant.split(successor)[0].rstrip()
                    comma_check = len(first_name) - 1
                    print('comma at index: ', comma_check)

                    if defendant[comma_check] == ',':
                        print('yes, there is a comma')
                        first_name = defendant[:comma_check]

                    print('first name: ', first_name)

                    successor_name = defendant[successor_start_index:].lstrip()
                    print('second name: ', second_name)
                    # new = name.split(fka, name)
                    # element1 = line.split(r'f/k', 1)[0].lstrip()  # 'f/k/a' for f/ or '(' for (f/k/a
                    # element2 = line.split('f/k/a', 1)[-1].rstrip(')').lstrip()
                    print('new string')

                    element1 = first_name
                    element3 = successor_name

                    break






        next_defendant = [element1, element2, element3, element4]
        list_of_Defendants.append(next_defendant)



    #if re.search('d/b/a', defendant):
    #    print("yes, there is dba'")
    #    element1 = defendant.split(r'(', 1)[0].lstrip()
    #    element3 = defendant.split('/a', 1)[-1].rstrip(')').lstrip()

    #else:
    #    print("nope, no dba")

    #print(sentence_list)

    #print(list_of_Defendants)
    # list_of_Defendants = [list_of_Defendants for defendants][0]
    print((list_of_Defendants))

    with open('test2_v2File.csv', 'a+', newline='') as result_file:
        wr = csv.writer(result_file)  # , dialect='excel')
        for row in open("test2_v2File.csv"):
            row_count += 1
        print('row count: ', row_count)
        for i in list_of_Defendants:
            wr.writerows([i])
