import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
from itertools import islice
import csv
import os
import glob
import pdftotext
# import textract
import codecs

#added if 'and' in last defendant, so split properly
#figure out how to get case 2-cv-XXXXX over case no: 21stvXXXXX | maybe if in earlier part of page

#will write to csv that the pdf was not read
def error_file_write(file_write):
    with open('MiguelAugustRun.csv', 'a+', newline='') as result_file:
        wr = csv.writer(result_file)  # , dialect='excel')
        element1 = 'File'
        element2 = 'Not'
        element3 = 'Read'
        element4 = file_write
        element5 = 'NULL'
        next_defendant = [element1, element2, element3, element4, element5]
        # print(list_of_Defendants)
        list_of_Defendants = []
        list_of_Defendants.append(next_defendant)
        for i in list_of_Defendants:
            wr.writerows([i])


def name_remover(fka, defendant):
    print(fka, ' found, removing ', defendant, ' from list')
    defendant.remove(defendant)
    print('names in list: ', defendant)
    print('')


#will check if semi-colons are present.
#if yes, hopefully these is what separates one defendant from the next
def semi_colon_checker(text):
    print('at checker')
    if ';' in text:
        print('yes it is')
        defendants = [defendant.lstrip().rstrip() for defendant in re.split(';', text)]
        global semi_colon_flag
        semi_colon_flag = True
        # return(semi_colon_flag)


case_index = ['case no\.', 'case', 'case no', 'INDEX NO\.', 'index', 'CAUSE NO\.', 'NO\.', 'CASE ID:']
vs_test_dict = ['vs\.', 'v\.', '-against', 'against \\n', 'versus\\n']
delimiter_dict = ['Company', 'INCORPORATED', 'Inc.', 'L.P.', 'LP', 'LLC', 'L.L.C.', 'Corporation', 'Co.', \
                  'Ltd', 'PLC', 'PBC', 'P.C.', 'L.L.C', 'S.A.', 'U.S.A.', 'USA', 'Inc']
fka_dict = ['f/k/a', 'fka', 'd/b/a', 'dba', 'd.b.a.']
successor_dict = ['individu', 'successo']  # for 'individually and as successor', 'successor-in-interest'

plaintiff_dict = ['Plaintiff\,', 'Plaintiffs\,', 'Plaintiff\\n,', 'Plaintiffs\\n,', 'Plaintiff', 'Plaintiffs']
defendants_dict = ['Defendant\.', 'Defendants\.', '\\nDefendant\\n', '\\nDefendants\\n', 'Defendant\\n',
                   'Defendants\\n', 'Defendant', 'Defendants']

first_line_present = False
files = [file for file in glob.glob("/Users/miguelgarcia/Desktop/Work/LitigationTracking/September-October/complaints-20221004-MiguelRun/Cut/*")]

complaint_num = 1

'''
This code is to extract defendants from legal documents,

Theoretically, we would like the steps to follow as
1.) Read in PDF document
2.) Script searches for the keywords 'plaintiff', 'vs', & 'defendant' - preferably in this order
3.) If found, the Defendants we are seeking (listed between 'plaintiff, vs' & 'defendant' should be extracted
4.) docket number will be extracted so we can identify case-defendant
5.) information will be output: defendant, any other names, documentName, docketNumber, defendantOrder 
'''


for file_name in files:
    list_of_Defendants = []

    # writes the first line so we can tell where runs stops and starts
    if first_line_present == False:
        run_differentiator = ['this', 'is', 'the', 'next', 'run']
        headers = ['DefendantName', 'F/K/A_or_D/B/A', 'Successor', 'DocName', 'CaseNumber', 'DefendantOrder', 'ComplaintOrder']
        list_of_Defendants.append(run_differentiator)
        list_of_Defendants.append(headers)

    semi_colon_flag = False
    reader = None
    file_string = str(file_name)  # using 'file' in reader variable was not reading the file/returned NoneType
    print("file is: ", file_string)

    if file_string == '.DS_Store':  # functions as a sort of error exception, this was stopping the code
        continue

    file_write = os.path.basename(os.path.normpath(file_string))

    first_line_present = True
    try:
        # pdf_file = open(file,'rb')
        with open(file_string, "rb") as f:
            reader = pdftotext.PDF(f)

    except IOError:
        print("Could not read file: ", file_string)
        print(type(reader))
        error_file_write(file_write)
        continue

    # Extract text and do the search
    # switch the pages loop to outer, vs loop to inner
    # page loop
    # plaintiff
    # vs loop
    # defendant loop

    # Where the keywords are located
    vs_pages = []  # where vs is present
    vs_plaintiff_pages = []  # where vs AND plaintiff are present
    # plaintiff_pages = []
    defendant_pages = []
    plaintiff_pages = []

    plain_def_vs_pages = []
    plain_vs_only_pages = []
    def_after_plain_vs = []
    def_after_plain_pages = []

    # will stop the loops from running for vs and def variables if found
    vs_done = False
    def_done = False
    case_num_done = False
    vs_plain_check = False
    plain_done = False

    # will keep these variations fixed to speed up
    vs_used = None
    def_used = None
    plain_used = None
    no_vs_used = None

    # using the present_vs/plaintiff/defendant
    present_vs = None
    present_plaintiff = None
    present_defendant = None

    # case_number
    case_number = None

    print('reading file: ', file_string)
    print(type(reader))
    NumPages = len(reader)
    #page1 = reader.getPage(0)
    page1Data = reader[0]
    # page1Data = textract.process(page1Data)
    print([page1Data])

    for i in range(NumPages):
        #curr_page = reader.getPage(i)
        curr_page_text = reader[i]
        curr_page_text = curr_page_text.replace('\n', '')
        # print('on page index: ', i)

        if case_num_done == False:
            for case in case_index:
                present_case = re.search(case, curr_page_text, flags=re.IGNORECASE)
                case_location = re.search(case, curr_page_text, flags=re.IGNORECASE)
                # print(present_case, "is present")
                # print('vs location: ', case_location)

                if present_case:  # is present/ == True
                    # print('hi')
                    case_start_index = present_case.start()
                    case_string_index = present_case.end()
                    case_string_end_index = case_start_index + 30
                    case_rough = curr_page_text[case_start_index:case_string_end_index]
                    case_rough = case_rough.replace('\n', '')

                    case_finer = None

                    # make sure you can only go here IF cv is in the 'case' variable
                    try:
                        cv_search = re.search('cv', case_rough, flags=re.IGNORECASE)  # looks for 'cv'

                        if cv_search:  # is present/ == True
                            cv_case = re.search(case, case_rough, flags=re.IGNORECASE)
                            cv_case_end_index = cv_case.end()
                            new_rough = case_rough[cv_case_end_index:].lstrip()

                            if new_rough[0] == ":":
                                new_rough = new_rough[1:].lstrip()

                            needs_work = False
                            while needs_work == False:  # trying to keep the '-DSF-PJW' in 2:20-cv-03317-DSF-PJW to prevent possible duplicates
                                # maybe just do a if ' ' in new_rough
                                if new_rough[-1].isalpha() or new_rough[-1] == '-' or new_rough[-1].isspace():
                                    if ' ' in new_rough:
                                        new_rough = new_rough[0:-1]
                                    else:
                                        needs_work = True
                                else:
                                    needs_work = True

                            numbersInCase = sum(i.isdigit() for i in new_rough)

                            if numbersInCase >= 4:
                                case_num_done = True

                            elif numbersInCase <= 3:
                                continue

                            case_finer = new_rough.rstrip()
                            case_number = case_finer
                            break

                        ###out of cv_search loop
                        case_finer = case_rough.rstrip()
                        try:
                            case_number_digit = sum(i.isdigit() for i in case_number)
                        except TypeError:
                            case_number_digit = 0

                        case_finer_digit = sum(i.isdigit() for i in case_finer)

                        if case_finer_digit > case_number_digit:
                            case_number = case_rough.rstrip()
                            case_number = case_finer

                        if not case_number:  # if case_number is None
                            case_number = case_finer

                    except:
                        try:
                            case_number_digit = sum(i.isdigit() for i in case_number)
                        except TypeError:
                            case_number_digit = 0

                        case_finer_digit = sum(i.isdigit() for i in case_finer)

                        if case_finer_digit > case_number_digit:
                            case_number = case_rough.rstrip()

                        if case_num_done == True:
                            break

        if vs_done == False:
            for vs in vs_test_dict:
                pattern = "rB'" + vs + "'"  # need to 'B' to make sure the string ends in the above in vs_dict
                # print(pattern)
                search_string = re.compile(pattern)
                present_vs = re.search(vs, curr_page_text, flags=re.IGNORECASE)
                vs_location = re.search(vs, curr_page_text, flags=re.IGNORECASE)
                # print(present_vs, "is present")
                # print('vs location: ', vs_location)

                # vs_pages = [] #where vs is present
                # vs_plaintiff_pages = [] #where vs AND plaintiff are present

                text1 = None

                if present_vs:  # finds the vs./against/v. | looking to find page naming plaintiffs vs defendants
                    for x in range(0, NumPages):
                        #PageObj1 = reader.getPage(x)
                        text1 = reader[x]
                        text1 = text1.replace('\n', '')
                        if re.search(vs, text1, flags=re.IGNORECASE):
                            # print(vs, " Found on Page: " + str(x))
                            vs_pages.append(x)
                            vs_used = vs
                            # vsPage = i

                    # exits loop when vs variable is found
                    break

        plaint_vs_test = None
        if vs_plain_check == False and plain_done == False:
            for vs_page in vs_pages:
                vs_plain_check = False
                if plain_done == False:
                    for plaintiff in plaintiff_dict:
                        #PageObj1 = reader.getPage(vs_page)
                        plaint_vs_test = reader[vs_page]
                        plaint_vs_test = plaint_vs_test.replace('\n', '')

                        # should we check if present_defendant is after plaintiff and vs on page???
                        present_plaintif = re.search(plaintiff, plaint_vs_test, flags=re.IGNORECASE)
                        if present_plaintif:
                            # print(vs_used,  "AND ", plaintiff, "Found on Page: " + str(vs_page))
                            # vs_plaintiff_pages.append(vs_page)
                            vs_done = True
                            vs_plain_check = True
                            plain_done = True
                            plain_used = plaintiff
                            break
                            # get out of finding 'plaintiff' loop

                        # vsPage = i
                if plain_done == True:  # when 'plaintiff' on same page as 'vs' is found, looks for other vs_pages where both occur
                    #PageObj1 = reader.getPage(vs_page)
                    plaint_vs_test = reader[vs_page]
                    plaint_vs_test = plaint_vs_test.replace('\n', '')

                    present_plaintif = re.search(plain_used, plaint_vs_test, flags=re.IGNORECASE)
                    if present_plaintif:
                        vs_plaintiff_pages.append(vs_page)

                # print(vs_used,  "AND ", plaintiff, "Found on Page: " + str(vs_page))
                # vs_plaintiff_pages.append(vs_page)

                if vs_plain_check == True:
                    break

        # is there is no 'vs' in the document, will go here
        if vs_plain_check == False and plain_done == False:  # if there is no 'vs'
            for plaintiff in plaintiff_dict:
                this_plain_leave_loop = False

                present_plaintiff = re.search(plaintiff, curr_page_text, flags=re.IGNORECASE)
                if present_plaintiff:
                    for x in range(0, NumPages):
                        #PageObj1 = reader.getPage(x)
                        text1 = reader[x]
                        text1 = text1.replace('\n', '')
                        text1 = text1.replace('Attorneys for Plaintiffs', 'AttorneysforPlaintiffs').replace('Attorney for Plaintiffs', 'AttorneyforPlaintiffs')
                        if re.search(plaintiff, text1, flags=re.IGNORECASE):
                            plaintiff_pages.append(x)
                            plain_done = True
                            plain_used = plaintiff
                            this_plain_leave_loop = True

                if this_plain_leave_loop == True:
                    break

        if def_done == False:
            for defendant in defendants_dict:
                pattern = "rB'" + defendant + "'"  # need to 'B' to make sure the string ends in the above in vs_dict
                # print(pattern)
                # curr_page_text is still on the original i, so still on page 1 of the doc(big bias towards first use of 'defendant'

                search_string = re.compile(pattern)
                present_defendant = re.search(defendant, curr_page_text, flags=re.IGNORECASE)
                def_location = re.search(defendant, curr_page_text)
                # print(present_defendant, "is present")
                # print(defendant, " location: ", def_location)
                # l = [curr_page_text]
                # print([curr_page_text])

                # should we be checking only the defendant pages after 'plaintiff' and 'vs'???
                if present_defendant:
                    for x in range(0, NumPages):
                        #PageObj1 = reader.getPage(x)
                        text1 = reader[x]
                        text1 = text1.replace('\n', '')
                        # text1 = textract.decode('utf')
                        if re.search(defendant, text1, flags=re.IGNORECASE):
                            # print(defendant, " Found on Page: " + str(x))
                            defendant_pages.append(x)
                            def_used = defendant
                            def_done = True
                            # vsPage = i
                    # exits loop when defendant variable is found
                    break

        # if we found all three, we will stop checking other pdf pages
        if vs_done == True and plain_done == True and def_done == True and case_num_done == True:
            break

    # out of loop finding 'vs', 'plaintiff, 'defendant'
    print('vs pages: ', vs_pages)
    print('vs plaintiff pages: ', vs_plaintiff_pages)
    print('defendant page: ', defendant_pages)
    print('plaintiff pages: ', plaintiff_pages)

    # end of reading loop, now we should only have the pages we want
    case1 = False
    case2 = False
    case3 = False

    all_three = None
    pdv_too_late = None
    error_index_all_three = None
    """
    pdv_too_late
    helps in instances where all three occur on page 53, when defendants were earlier in doc
    think "plaintiff-versus" happens on first page, then defendants on 2nd page BUT then all three occur on page 53
    page 53 wont be useful, those are just keywords.
    """

    # this is a set, will need to be turned into a list later
    plain_vs_def = set(vs_pages) & set(vs_plaintiff_pages) & set(defendant_pages)

    if plain_vs_def:  # All three have at least one value in common
        print("all three occur on page(s): ", plain_vs_def)
        print(type(plain_vs_def))
        all_three = True
        for page in plain_vs_def:
            plain_def_vs_pages.append(page)

            # case1 = True

    # if case1 == False: #goes here only if case1 didnt equate to True
    plain_vs_only = set(vs_pages) & set(vs_plaintiff_pages)
    for page in plain_vs_only:
        plain_vs_only_pages.append(page)

    # change to for loop, get all 'defendant' uses after 1st instance of plaintiff_vs
    # [0] <= [1]
    # def_page_after = 1
    try:
        if plain_vs_only_pages[0] <= defendant_pages[0]:
            # if first instance of 'defendant' comes after a 'plaintiff & vs' combo, we probably shouldnt use that
            print(def_used, ' comes after plaintiff and ', vs_used)

            def_page_after = defendant_pages[0]  # ex plaintiff on page 1, defendants on page 2

    except IndexError:
        pass

        # case2 = True
    # ex, plain_def_vs_pages = [51], def_page_after = [1]
    if not plain_def_vs_pages:  #
        print('All 3 do not occur on a single page')
        all_three = False

    try:
        if def_page_after < plain_def_vs_pages[0]:
            # what if [0] < [0]
            # good: [1] < [0]
            # [0] < [56]
            # trying to get earliest plaintiff, vs, defendant.
            # some problems were all three occuring on page 53, when listed defendants would be around pages 1-4
            # so, if [53] <= [2] we avoid this problem
            # but if [1] <= [2] we proceed with the good
            print('checking to see something')
            pdv_too_late = True  # plain_def_vs_pages

        elif def_page_after >= plain_def_vs_pages[0]:
            # [5] >= [5]
            # [6] >= [56]
            pdv_too_late = False

    except IndexError:
        print('index error')
        error_index_all_three = True
    except NameError:
        pass

    if error_index_all_three == True:
        try:
            for defendant_page in defendant_pages:
                if defendant_page < plain_vs_only_pages[0]:
                    # what if [0] < [0]
                    # good: [1] < [0]
                    # [0] < [56]
                    # trying to get earliest plaintiff, vs, defendant.
                    # some problems were all three occuring on page 53, when listed defendants would be around pages 1-4
                    # so, if [53] <= [2] we avoid this problem
                    # but if [1] <= [2] we proceed with the good
                    print('checking to see something')
                    pdv_too_late = True  # plain_def_vs_pages

                elif defendant_page >= plain_vs_only_pages[0]:
                    # [5] >= [5]
                    # [6] >= [56]
                    pdv_too_late = False

        except:
            continue

    # elif case2 == False:
    #    case1 = True

    if all_three == True and pdv_too_late == False:
        case1 = True

    elif all_three == False and pdv_too_late == True:  # and
        if case1 == False:
            case2 = True

    elif all_three == False and pdv_too_late == False:
        if case1 == False:
            case2 = True

    elif case1 == False and case2 == False:  # if there is no 'vs' variable
        for defendant_page in defendant_pages:  # for no 'vs'
            int_plain = int(len(plaintiff_pages))
            for plain_page in plaintiff_pages:
                try:
                    if defendant_page >= plaintiff_pages[plain_page]:
                        def_after_plain_pages.append(defendant_page)
                        def_after_plain_pages.append(plain_page)
                except IndexError:
                    pass

        def_after_plain_pages = list(set(def_after_plain_pages))  # eliminates duplicates
        def_after_plain_pages.sort()

        if plaintiff_pages[0] <= def_after_plain_pages[-1]:
            case3 = True

    # reader.close() # dont need to close the file???

    number_of_pages = None
    end_index = None
    start_index = None

    # ideally, case 1 happens when all three occur early in the pdf, trying to ignore cases where it happens in the end
    # case 2, happens when 'plaintiff&vs' happen, and 'defendant' occurs right after
    # case 3, the least likely, is first occurence where 1.) plaintiff, 2.) vs,3.) defendant

    if case1 == True:
        number_of_pages = len(plain_def_vs_pages)
        end_index = (plain_def_vs_pages[-1]) + 1
        start_index = plain_def_vs_pages[0]

    elif case2 == True:
        number_of_pages = len(plain_vs_only_pages) + 1
        end_index = (defendant_pages[-1]) + 1
        start_index = plain_vs_only_pages[0]
        # print('hi')

    elif case3 == True:
        print('will do stuff')
        number_of_pages = len(def_after_plain_pages) + 1
        end_index = (defendant_pages[-1]) + 1
        start_index = plaintiff_pages[0]

    print("number of pages: ", number_of_pages, " start index: ", start_index, " end index: ", end_index)

    # this becomes the text from the pages, but as a string
    document_text = ''
    for page in islice(range(end_index), start_index,
                       end_index):  ##changed 'number_of_pages' to 'end_index' to resolved errors of not running loop
        print('on page: ', page)
        #page_num = reader.getPage(page)
        page_text = reader[page]
        # print('hi')
        # print(page_text)
        document_text += page_text
        # print(page_text)

    # document_text.encode('utf-8')
    # document_text.decode(encodings = 'utf-8')
    document_text = document_text.replace("™", "'").replace('\n', '')
    document_text = document_text.replace("‚Äô", "'")
    document_text = document_text.replace('Attorneys for Plaintiffs', 'AttorneysforPlaintiffs').replace(
        'Attorney for Plaintiffs', 'AttorneyforPlaintiffs')

    # see if 'vs' comes after plaintiff and defendant(ie, no 'vs'' that is of use to us)
    doc_text_plain_used = re.search(plain_used, document_text, flags=re.IGNORECASE)
    doc_text_vs_used = re.search(vs_used, document_text, flags=re.IGNORECASE)
    doc_text_def_used = re.search(def_used, document_text, flags=re.IGNORECASE)

    # doc_text_plain_used <= doc_text_vs_used <= doc_text_def_used
    try_no_vs = False
    if doc_text_plain_used and doc_text_def_used and not doc_text_vs_used:
        if doc_text_plain_used.end() < doc_text_def_used.start():
            try_no_vs = True

    try:
        if try_no_vs == False:
            flag_vs = vs_used.replace('\\', '')

        elif try_no_vs == True:
            flag_vs = plain_used.replace('\\', '')


    except AttributeError:
        no_vs_used = True
        flag_vs = plain_used.replace('\\', '')

    # removing everything before the 'plaintiff' variable
    try:
        document_text = document_text.split(flag_vs)[1]

    except IndexError:  # easier to find index and cut from there than replace up top
        vs_index_start = re.search(vs_used, document_text, flags=re.IGNORECASE).start()
        vs_index_end = re.search(vs_used, document_text, flags=re.IGNORECASE).end()
        document_text = document_text[vs_index_end:]

    # removing text after 'defendant' variable (list of defendants)
    flag_def = def_used.replace('\\n', '').replace('\\', '')
    try:
        document_text = document_text.split(flag_def)[0]

    except IndexError:  # easier to find index and cut from there than replace up top
        def_index_start = re.search(vs_used, document_text, flags=re.IGNORECASE).start()
        def_index_end = re.search(vs_used, document_text, flags=re.IGNORECASE).end()
        document_text = document_text[:def_index_start]

    print('doc text is: ', document_text)
    # print('names: ', text)

    # turns text(STRING) into a list to remove '\n' and turns it back into a string
    list = [document_text.replace('\n', '')]
    # print(list)
    text = document_text.join(list)
    # print(document_text)

    # next thing if plaintiff page #<= vs page # <= defendant page #

    comma_indexes = [x.start() for x in re.finditer(',', text)]
    # print(comma_indexes)  # <-- [6, 13, 19]

    sentence_list = []
    defendants = []
    # defendant_count = len(sentence_list)
    # print(defendant_count)

    # Will eliminate Commas from list of defendants if semi-colons are not present
    # will distinguish between companies with US., Inc. names
    # will also keep names if FKA / DBA is present
    text
    semi_colon_checker(text)

    # defendants = [sentence.lstrip().replace('\n', '') for sentence in re.split(';', text)]

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

        next_comma = None
        try:
            next_comma = comma_indexes[curr_index + 1]
        except IndexError:
            next_comma = len(text)
        # next_comma = comma_indexes[curr_index + 1]
        # area_between_index = text[next_comma]

        name_in_question = text[start_index:end_index]
        print('name in question: ', name_in_question)

        break_loop_flag = False
        for fka in fka_dict:
            for delimeter in delimiter_dict:
                if text[end_index] == ',' and (
                        fka.casefold() in search_area.casefold() or delimeter.casefold() in search_area.casefold()):
                    # print(text[start_index:end_index])
                    # print("yes there is a comma at index: ", end_index, ' and other name in search area: ', search_area)
                    end_index = next_comma

                    try:  # was a problem with the last text sometimes
                        search_end = end_index + 10
                    except TypeError:
                        pass

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

    # print(text)
    # print(comma_indexes)

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
            next_comma = len(text)
            # next_comma = len(text) ??????

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
    # print(text)
    # defendants = re.split(';', text).lstrip()
    defendants = [defendant.lstrip().rstrip() for defendant in re.split(';', text)]  # need to get rid of whitespace

    # print(defendants)

    defendant_count = len(defendants)
    # print(defendant_count)

    index_def_count = defendant_count - 1

    # elimanates any 'and's in the beginning of defendant names
    for defendant in defendants:
        curr_def_index = defendants.index(defendant)
        curr_def = defendants[curr_def_index]
        print(curr_def)

        and_pattern = re.compile("r'^and\s'")

        potential_and_checker = re.match(r'^and', curr_def, flags=re.IGNORECASE)
        if potential_and_checker:  # add ignore case? replace by indexes?
            print('yes it does')
            # potential_and = curr_def.replace("and", "").lstrip()
            potential_and = curr_def[potential_and_checker.end():]  # removes any 'And'
            potential_and = potential_and.lstrip()
            defendants[curr_def_index] = potential_and
            # print(curr_def)
    # print(defendants)

    # eliminates 'and' anywhere in defendant name and will split them there
    for defendant in defendants:
        curr_def_index = defendants.index(defendant)
        curr_def = defendants[curr_def_index]

        and_check = re.search('and', curr_def)  # we only want 'and', thus will not case ignore

        if and_check:  # yes, 'and; is here
            successor_check = False
            fka_check = False

            # these two checks to make sure we keep FKA/DBAs or 'and as succesor' in tact
            for successor in successor_dict:
                if re.search(successor, curr_def, flags=re.IGNORECASE):  # if 'and as successor' it will skip the cut
                    successor_check = True
                    break

            if successor_check == True:
                continue

            for fka in fka_dict:
                if re.search(fka, curr_def, flags=re.IGNORECASE):
                    fka_check = True
                    break

            if fka_check == True:
                continue

            and_start_ind = and_check.start()
            and_end_ind = and_check.end()
            defendants.remove(curr_def)

            first_and_def = curr_def[:and_start_ind]
            first_and_def = first_and_def.rstrip()

            sec_and_def = curr_def[and_end_ind:]
            sec_and_def = sec_and_def.lstrip()

            first_add_index = curr_def_index
            sec_add_index = curr_def_index + 1

            defendants.insert(first_add_index, first_and_def)
            defendants.insert(sec_add_index, sec_and_def)

    # will get rid of empty strings
    try:
        defendants.remove('')
    except ValueError:
        pass

    # will separate defendants into fka/dba(s), successors,
    # list_of_Defendants = [] || moved to the top

    # writes names to file
    def_order_num = 1

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
        element4 = file_write
        element6 = def_order_num
        element7 = complaint_num

        def_order_num += 1

        try:
            element5 = case_number

        except:
            element5 = 'NULL'

        for fka in fka_dict:
            if re.search(fka, defendant):  # do some regex magiv for fka, f/k/a, FKA, F/K/A, etc
                # Prevents skipping/cannot remove items while iterating
                # will removing from names[] list
                # But, will be going over all names because they remain unchanged in the copy of the list
                done = False

                # print('current name: ', defendant)
                # print("yes, there is: ", fka)

                fka_start_index = re.search(fka, defendant, flags=re.IGNORECASE).start()
                # print(fka, 'start index: ', fka_start_index)
                parenthesis_check = fka_start_index - 1
                # print('parenthesis index: ', parenthesis_check)

                if defendant[parenthesis_check] == '(':
                    print('yes parenthesis')

                    comma_check = parenthesis_check - 1
                    if defendant[comma_check] == ',':
                        print('yes, there is a comma')
                        defendant = defendant[:comma_check] + defendant[comma_check + 1:]

                    first_name = defendant.split('(', 1)[0].rstrip()
                    # print('first name: ', first_name)

                    pattern = '(' + fka
                    # print('pattern :', pattern)
                    second_name = defendant.split(pattern, 1)[-1].lstrip().rstrip(')')
                    # print('second name: ', second_name)

                    second_name = fka + ": " + second_name

                    element1 = first_name
                    element2 = second_name

                    break

                else:
                    print('no parenthesis')
                    #for uppercase, maybe replace by indeex? or convert to upper or lower
                    first_name = defendant.split(fka)[0].rstrip()
                    comma_check = len(first_name) - 1
                    print('comma at index: ', comma_check)

                    if defendant[comma_check] == ',':
                        print('yes, there is a comma')
                        first_name = defendant[:comma_check]

                    print('first name: ', first_name)

                    second_name = defendant.split(fka)[-1].lstrip()
                    print('second name: ', second_name)
                    # new = name.split(fka, name)
                    # element1 = line.split(r'f/k', 1)[0].lstrip()  # 'f/k/a' for f/ or '(' for (f/k/a
                    # element2 = line.split('f/k/a', 1)[-1].rstrip(')').lstrip()
                    print('new string')
                    second_name = fka + ": " + second_name

                    element1 = first_name
                    element2 = second_name

                    break

                # x = len(re.search('f/k/a'))
                # element1 = defendant.split(r'(')[0].lstrip()
                # element2 = defendant.split(fka, 1)[-1].rstrip(')').lstrip()
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
                    # print('second name: ', second_name)

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
                    # print('second name: ', second_name)
                    # new = name.split(fka, name)
                    # element1 = line.split(r'f/k', 1)[0].lstrip()  # 'f/k/a' for f/ or '(' for (f/k/a
                    # element2 = line.split('f/k/a', 1)[-1].rstrip(')').lstrip()
                    print('new string')

                    element1 = first_name
                    element3 = successor_name

                    break

        # Gets ride of leading '-' in '- 3M Company'
        if vs_used == '-against':
            try:
                if element1[0] == '-':  # trying to eleminate remaining '-' in '-against-'
                    element1 = element1[1:]  # gets of '-'
                    element1 = element1.lstrip()  # gets rid of whitespace
                    # '- 3M' -> '3M'
            except IndexError:
                pass


        next_defendant = [element1, element2, element3, element4, element5, element6, element7]
        list_of_Defendants.append(next_defendant)

    print((list_of_Defendants))
    complaint_num += 1

    #will write case, defendants, and docketnumber to csv file for current pdf
    with open('MiguelAugustRun.csv', 'a+', newline='', encoding='utf-8') as result_file:
        wr = csv.writer(result_file)  # , dialect='excel')
        # for row in open("test2_v2File.csv"):
        # row_count += 1
        # print('row count: ', row_count)
        for i in list_of_Defendants:
            wr.writerows([i])
