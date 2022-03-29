if re.search(fka, defendant):
            #done = False

            #print('found ', fka)

            #fka_start_index = re.search(fka, defendant, flags=re.IGNORECASE).start()
            #print(fka, 'start index: ', fka_start_index)

            #parenthesis_check = fka_start_index - 1
            #print('parenthesis index: ', parenthesis_check)

            if defendant[parenthesis_check] == '(':
                print('yes parenthesis')

                first_name = defendant.split('(', 1)[0]
                print('first name: ', first_name)

                pattern = '(' + fka
                print('pattern :', pattern)
                second_name = name.split(pattern, 1)[-1].lstrip().rstrip(')')
                print('second name: ', second_name)

                done = True


            else:
                print('no parenthesis')
                second_name = defendant.split(fka)[0]
                print('first name: ', second_name)

                second_name = defendant.split(fka)[-1].lstrip()
                print('second name: ', second_name)
                #new = name.split(fka, name)
                #element1 = line.split(r'f/k', 1)[0].lstrip()  # 'f/k/a' for f/ or '(' for (f/k/a
                #element2 = line.split('f/k/a', 1)[-1].rstrip(')').lstrip()
                print('new string')

                done = True

            #name = name -1
            if done:
                name_remover(fka, defendant)


            print('')

        else:
            print('did not find ', fka)