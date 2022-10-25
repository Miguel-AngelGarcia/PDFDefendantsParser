import textract
import os
import re
from itertools import islice
import csv
import glob

def error_file_write(file_write):
    with open('testPDFcutter.csv', 'a+', newline='') as result_file:
        wr = csv.writer(result_file)  # , dialect='excel')
        element1 = 'File'
        element2 = 'Not'
        element3 = 'Read'
        element4 = file_write
        element5 = 'NULL'
        next_defendant = [element1, element2, element3, element4, element5]
        #print(list_of_Defendants)
        list_of_Defendants = []
        list_of_Defendants.append(next_defendant)
        for i in list_of_Defendants:
            wr.writerows([i])

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

case_index = ['case no\.', 'case', 'case no', 'INDEX NO\.', 'index', 'CAUSE NO\.', 'NO\.', 'CASE ID:']
vs_test_dict = ['vs\.', 'v\.', '-against', 'against \\n', 'versus\\n']
delimiter_dict = ['Company', 'INCORPORATED', 'Inc.', 'L.P.', 'LP', 'LLC', 'L.L.C.', 'Corporation', 'Co.', 'Ltd']
fka_dict = ['f/k/a', 'fka', 'd/b/a', 'dba']
successor_dict = ['individu', 'successo']  # for 'individually and as successor', 'successor-in-interest'

plaintiff_dict = ['Plaintiff\,', 'Plaintiffs\,', 'Plaintiff\\n,', 'Plaintiffs\\n,', 'Plaintiff', 'Plaintiffs']
defendants_dict = ['Defendant\.', 'Defendants\.', '\\nDefendant\\n', '\\nDefendants\\n', 'Defendant\\n', 'Defendants\\n']

files = [file for file in glob.glob("/Users/miguelgarcia/Desktop/Work/LitigationTracking/JuneComplaints/JunesFirstBatch/JuneComplaintsEdit/*")]

first_line_present = False

for file_name in files:
    list_of_Defendants = []

    # writes the first line so we can tell where runs stop and start
    if first_line_present == False:
        run_differentiator = ['this', 'is', 'the', 'next', 'run']
        list_of_Defendants.append(run_differentiator)

    semi_colon_flag = False
    reader = None
    file_string = str(file_name)  # using 'file' in reader variable was not reading the file/returned NoneType
    print("file is: ", file_string)

    if file_string == '.DS_Store':  # functions as a sort of error exception, this was stopping the code
        continue

    file_write = os.path.basename(os.path.normpath(file_string))

    first_line_present = True
    try:
        reader = textract.process(file_string)
        reader = reader.decode('utf-8')
        print(reader)
        #type = type(reader)

        if reader is None:
            print('Is NoneType, thus not readable')

    except IOError:
        print("Could not read file: ", file_string)
        #print(type(reader))
        #error_file_write(file)
        continue

        # Extract text and do the search
        # siwtch the pages loop to outer, vs loop to inner
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
    NumPages = reader.getNumPages()
    page1 = reader.getPage(0)
    page1Data = page1.extractText()
    # page1Data = textract.process(page1Data)
    print([page1Data])

    for i in range(NumPages):
        curr_page_text = reader[i]
        #curr_page_text = curr_page.extractText()
        curr_page_text = curr_page_text.replace('\n', '')

        if case_num_done == False:
            for case in case_index:
                present_case = re.search(case, curr_page_text, flags=re.IGNORECASE)
                case_location = re.search(case, curr_page_text, flags=re.IGNORECASE)
                #print(present_case, "is present")
                #print('vs location: ', case_location)


                if present_case:  # is present/ == True
                    print('hi')
                    case_indexes = [x.start() for x in re.finditer(case, reader, re.IGNORECASE)]

                    for case_num in case_indexes:
                        case_start_index = case_num
                        case_string_index = case_num + len(case) #ie 'case no.' = 8, so 0 + 8
                        case_string_end_index = case_start_index + 30
                        case_rough = reader[case_start_index:case_string_end_index]

                        # make sure you can only go here IF cv is in the 'case' variable
                        try:
                            cv_search = re.search('cv', case_rough, flags=re.IGNORECASE)  # looks for 'cv'

                            if cv_search:  # is present/ == True
                                cv_case = re.search(case, case_rough, flags=re.IGNORECASE)
                                cv_case_end_index = cv_case.end()
                                new_rough = case_rough[cv_case_end_index:].lstrip()
                                #new_rough = 'is a mention of'

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
                #print(pattern)
                search_string = re.compile(pattern)
                present_vs = re.search(vs, curr_page_text, flags=re.IGNORECASE)
                vs_location = re.search(vs, curr_page_text, flags=re.IGNORECASE)
                #print(present_vs, "is present")
                #print('vs location: ', vs_location)

                #vs_pages = [] #where vs is present
                #vs_plaintiff_pages = [] #where vs AND plaintiff are present

                text1 = None

                if present_vs: #finds the vs./against/v. | looking to find page naming plaintiffs vs defendants
                    for x in range(0, NumPages):
                        PageObj1 = reader.getPage(x)
                        text1 = PageObj1.extractText()
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
                        PageObj1 = reader.getPage(vs_page)
                        plaint_vs_test = PageObj1.extractText()
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
                    PageObj1 = reader.getPage(vs_page)
                    plaint_vs_test = PageObj1.extractText()
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
                                PageObj1 = reader.getPage(x)
                                text1 = PageObj1.extractText()
                                text1 = text1.replace('\n', '')
                                text1 = text1.replace('Attorneys for Plaintiffs', 'AttorneysforPlaintiffs').replace(
                                    'Attorney for Plaintiffs', 'AttorneyforPlaintiffs')
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
                print(pattern)
                search_string = re.compile(pattern)
                present_defendant = re.search(defendant, curr_page_text)
                def_location = re.search(defendant, curr_page_text)
                print(present_defendant, "is present")
                print(defendant, " location: ", def_location)
                l = [curr_page_text]
                print([curr_page_text])

                # should we be checking only the defendant pages after 'plaintiff' and 'vs'???
                if present_defendant:
                    for x in range(0, NumPages):
                        text1 = reader[x]
                        #text1 = PageObj1.extractText()
                        if re.search(defendant, text1, flags=re.IGNORECASE):
                            print(defendant, " Found on Page: " + str(x))
                            defendant_pages.append(x)
                            def_used = defendant
                            def_done = True
                            # vsPage = i
                    # exits loop when defendant variable is found
                    break
        # if we found all three, we will stop checking other pdf pages
        if vs_done == True and plain_done == True and def_done == True and case_num_done == True:
            break

    print('vs pages: ', vs_pages)
    print('vs plaintiff pages: ', vs_plaintiff_pages)
    print('defendant page: ', defendant_pages)

    # end of reading loop, now we should only have the pages we want
    case1 = False
    case2 = False
    case3 = False

    all_three = None
    pdv_too_late = None
    """
    pdv_too_late
    helps in instances where all three occur on page 53, when defendants were earlier in doc
    think plaintiff versus happens on first page, then defendants but all three ovvur on page 53
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
    if plain_vs_only_pages[0] <= defendant_pages[0]:
        # if first instance of 'defendant' comes after a 'plaintiff & vs' combo, we probably shouldnt use that
        print(def_used, ' comes after plaintiff and ', vs_used)

        def_page_after = defendant_pages[0]  # ex plaintiff on page 1, defendants on page 2

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
            pdv_too_late = True

    except IndexError:
        print('index error')

    # elif case2 == False:
    #    case1 = True

    if all_three == True and pdv_too_late == False:
        case1 = True

    if all_three == False and pdv_too_late == True:  # and
        case2 = True

    # reader.close() # dont need to close the file???

    number_of_pages = None
    end_index = None
    start_index = None

    # ideally, case 1 happens when all three occur early in the pdf, tryinh to ignore cases where it happenbs in the end
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
        number_of_pages = len(plain_vs_only_pages) + 1
        end_index = (defendant_pages[-1]) + 1
        start_index = plain_vs_only_pages[0]

    print("number of pages: ", number_of_pages, " start index: ", start_index, " end index: ", end_index)

    # this becomes the text from the pages, but as a string
    document_text = ''
    for page in islice(range(number_of_pages), start_index, end_index):
        print('on page: ', page)
        page_num = reader.getPage(page)
        page_text = page_num.extractText()
        # print('hi')
        # print(page_text)
        document_text += page_text
        # print(page_text)

    flag_vs = vs_used.replace('\\', '')
    document_text = document_text.split(flag_vs)[1]
    # print(document_text)
    flag_def = def_used.replace('\\n', '').replace('\\', '')
    document_text = document_text.split(flag_def)[0]
    print('doc text is: ', document_text)
    # print('names: ', text)

    # turns text(STRING) into a list to remove '\n' and turns it back into a string
    list = [document_text.replace('\n', '')]
    print(list)
    text = document_text.join(list)
    print(document_text)

    # next thing if plaintiff page #<= vs page # <= defendant page #

    comma_indexes = [x.start() for x in re.finditer(',', text)]
    # print(comma_indexes)  # <-- [6, 13, 19]

    sentence_list = []
    defendants = []
    # defendant_count = len(sentence_list)
    # print(defendant_count)

    # Will eeminate Commas from list of defendants if semi-colons are not present
    # will distingiush between companies with US., Inc. names
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
                    print("yes there is a comma at index: ", end_index, ' and other name in search area: ',
                          search_area)
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
        if re.match(r'^and\s', curr_def):
            print('yes it does')
            potential_and = curr_def.replace("and", "").lstrip()
            # print(potential_and)
            #    print(potential_and)
            #    print(type(potential_and))
            defendants[curr_def_index] = potential_and
            # print(curr_def)
    # print(defendants)

    # will separate defendants into fka/dba(s), successors,
    list_of_Defendants = []

    # writes names to file
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
        element5 = case_number

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
                    # new = name.split(fka, name)
                    # element1 = line.split(r'f/k', 1)[0].lstrip()  # 'f/k/a' for f/ or '(' for (f/k/a
                    # element2 = line.split('f/k/a', 1)[-1].rstrip(')').lstrip()
                    print('new string')

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

        next_defendant = [element1, element2, element3, element4, element5]
        list_of_Defendants.append(next_defendant)

    # if re.search('d/b/a', defendant):
    #    print("yes, there is dba'")
    #    element1 = defendant.split(r'(', 1)[0].lstrip()
    #    element3 = defendant.split('/a', 1)[-1].rstrip(')').lstrip()

    # else:
    #    print("nope, no dba")

    # print(sentence_list)

    # print(list_of_Defendants)
    # list_of_Defendants = [list_of_Defendants for defendants][0]
    print((list_of_Defendants))

    with open('TESTTEST.csv', 'a+', newline='', encoding='utf-8') as result_file:
        wr = csv.writer(result_file)  # , dialect='excel')
        # for row in open("test2_v2File.csv"):
        # row_count += 1
        # print('row count: ', row_count)
        for i in list_of_Defendants:
            wr.writerows([i])

