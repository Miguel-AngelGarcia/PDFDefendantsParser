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