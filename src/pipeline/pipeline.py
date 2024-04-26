
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

def extract_lines():
    x1 = open('pipeline/X1.json', 'r')
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

    
    filepath = "sample_data/0b8706dc-c9af-4c6b-887d-2f85b5a511e7.txt"
    file = open(filepath, 'r')
    data = file.read()
    print(f"Number of characters in document: {len(data)}")
    print(f"First word just to check {data.split()[0]}")    

    lines = data.split('\n')

    found = {}
    for i, line in enumerate(lines):
        for word in line.split():
            if word.lower() in all_keywords:
                found[word] = line
    
    
    # Remove duplicates. All keys == Abrr

    final_found = {}

    for key in found.keys():
        for x in content:
            lowercase_synonyms = [item.lower() for item in x['Synonyms']]
            if key.lower() == x['Abbreviation'].lower() or key.lower() in lowercase_synonyms:
                final_found[x['Abbreviation']] = found[key]

    print(f"Length found = {len(final_found.keys())}")    
    print(80*'-')

    print(final_found)

    print(80*'-')
    return final_found

def create_template():

    # {"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}
    """
        Template:
            parameter: 
            value:
            unit:
    """
   
    lines =  extract_lines()

    
    return 

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

from pipeline.LLM import ollama_phi3
from pipeline.statistics import calculate_accuracy

if __name__ == "__main__":
    #create_template()

    lines = extract_lines()
    start_time = time.time()
    query = (
        f"""Context: You are a medical expert that specialises in extracting structured data from lab reports
            Task: For each key and value in the dictionary defined below fill out the template below.
                - The parameter is meant to be equal to the key in the dictionary
                - The value is meant to be a numeric from that line
                - The unit is meant to be the unit of measurement for the parameter

            Refer to the Example to see what the input output relationship is meant to be
            Example:
                Line: ["Total Testosterone": "Total Testosterone (Siemens) 39.2 nmol/L (8.3-29)"]
                Output: [{{"parameter": "Total Testosterone", "value": 39.2, "unit":"nmol/L"}}]

            
            Dictionary: [{lines}]

            Template: [{{"parameter":, "value":, "unit": }}]
            """
    )
    end_time = time.time()
    result = ollama_phi3(query)

    print(result)
    print('-'*80)

    num_results = len(result.split('\n'))
    print(f"Num results: {num_results}")

    print(f"Runtime: {(end_time - start_time)}")
    
    result = json.loads(result)

    acc = calculate_accuracy(result, "0b8706dc-c9af-4c6b-887d-2f85b5a511e7.txt")
    print(acc)