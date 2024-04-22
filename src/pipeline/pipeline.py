from statistics import percentage_char_extracted, num_params_ext

if __name__ == "__main__":

    with open('../sample_data/0b8706dc-c9af-4c6b-887d-2f85b5a511e7.txt', 'r') as file:
        content = file.read()
        print(content)
        print('-'*80)
        file.close()
        lines = content.split('\n')
        print(len(lines))

        test = [{"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}, {"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}, {"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}]
        print(percentage_char_extracted(test, content))
        print(num_params_ext(test))
