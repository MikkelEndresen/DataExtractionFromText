

if __name__ == "__main__":

    with open('../sample_data/0b8706dc-c9af-4c6b-887d-2f85b5a511e7.txt', 'r') as file:
        content = file.read()
        print(content)
        print('-'*80)
        file.close()
        lines = content.readlines()
        print(len(lines))

    print('-'*80)

    with open('../sample_data/0b8706dc-c9af-4c6b-887d-2f85b5a511e7.txt', 'r') as file:
        content = file.readlines()
        new_list = []
        for line in content:
            line = line.strip()
            if line != '' and line != '\n':
                new_list.append(line)
                print(line)

        print(len(content))
        print(len(new_list))
