
def pipeline(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
        #print(content)
       # print('-'*80)
        file.close()
        lines = content.split('\n')
        #print(len(lines))

        return [{"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}, {"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}, {"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}]


import json
import time

def create_template():

    # {"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}
    """
        Template:
            parameter: 
            value:
            unit:
    """
    # Try to specify which paramaters I am looking for by keyword recognition first.
    # exchange (parmater), with keyword found

    # TODO: vectorise X1.json to make the search for relevant keywords faster.
    # Looping through entire document for each keyword and synonym is going to be slow. 
    # In total there are 2694 keywords
    # Takes about 0.06 seconds to loop through the largest document. 

    # load X1.json

    x1 = open('X1.json', 'r')
    content = json.load(x1)
    print(f"Number of parameters: {len(content)}")
    print()

    all_keywords = []
    for parameter in content:
        #print(parameter['Abbreviation'])
        all_keywords.append(parameter['Abbreviation'].lower())
        for synonym in parameter['Synonyms']:
            all_keywords.append(synonym.lower())
            #print(synonym)
        #break
    
    print(f"Number of keywords: {len(all_keywords)}")

    start_time = time.time()

    filepath = "../sample_data/0b8706dc-c9af-4c6b-887d-2f85b5a511e7.txt"
    file = open(filepath, 'r')
    data = file.read()
    print(f"Number of characters in document: {len(data)}")
    print(f"First word just to check {data.split()[0]}")    

    lines = data.split('\n')

    found_method1 = {}
    found_method2 = []
    for i, line in enumerate(lines):
        for word in line.split():
            if word.lower() in all_keywords:
                found_method1[word] = line
                found_method2.append({'word': word, 'line': line})


    print(f"Length no overwrite = {len(found_method2)}")
    print(f"Length overwrite = {len(found_method1.keys())}")

    keys = [key['word'] for key in found_method2]
    print(keys)
    print(80*'-')
    print(found_method1.keys())
    
    print(80*'-')
    # Remove duplicates. All keys == Abrr

    final_found = {}

    for key in found_method1.keys():
        for x in content:
            lowercase_synonyms = [item.lower() for item in x['Synonyms']]
            if key.lower() == x['Abbreviation'].lower() or key.lower() in lowercase_synonyms:
                final_found[x['Abbreviation']] = found_method1[key]
                # temp_line = found_method1[key]
                # del(found_method1[key])
                # found_method1[x['Abbreviation']] = temp_line

    print(len(final_found.keys()))
    print(final_found.keys())
    """
    Desired format:
        Only one for each. So bump if already exists...?
    """

    return final_found

    found = []
    for word in content.split():
        word_to_check = word.lower()
        if word_to_check in all_keywords: # TODO: This misses two word combinations. e.g: "Troponin I"
            found.append(word.lower())

    print(f"Keywords found: {found}")
    end_time = time.time()

    runtime = end_time - start_time 
    print(f"It took {runtime} long to check the largest file given")

    # Isolate lines where it is found, give values

if __name__ == "__main__":
    create_template()