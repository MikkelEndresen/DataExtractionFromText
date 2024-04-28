from pipeline.utils import x1_data, x1_keywords,  extract_lines_from_unstructured, all_abbr
from pipeline.LLM import ollama_phi3
import json


import lmformatenforcer

def LLM_query(lines):
    """
    Description:
        - Defines the query for the LLM
    Input:
        - Lines. List of {'param': 'line_with_info'}
    Output:
        - Formatted query
    """
    query = f"""
        Find the parameter, value, and unit for each dictionary in the list under Input, and fill in the schema.
        - The value of "parameter" in the template should be equal to the key in the dictionary.
        - The value of "value" should be a numeric value extracted from the value in the dictionary.
        - The value of "unit" should be the unit of measurement for the parameter, also in the value in the dictionary.

    Refer to the Example to see the input-otput relationship. All output should be in JSON format of a list of dictionaries.
    Ensure all values are represented as strings with double quotations. 

    Examples:
        Input [{{"Total Testosterone": "Total Testosterone (Siemens) 39.2 nmol/L (8.3-29)"}}, {{"Iron": "Iron (10-30) umol/L 40 33 21 27"}}]
        Output: [{{"parameter": "Total Testosterone", "value": 39.2, "unit": "nmol/L"}}, {{"parameter": "Iron", "value": 27, "unit": "umol/L"}}]

    Input: {lines}

    Schema: [{{"parameter":text, "value":float , "unit":text}}, {{"parameter":text, "value":float , "unit":text}}...]
    """

    return query

def standardise_result(result):
    """
    Description:
        - Making sure there are no key errors. 
    Input:
        - result list of dictionaries
    Output:
        - List of dictionaries:  {"parameter":, "value":, "unit":}
    """

    new_result = []
    for item in result:
        
        if isinstance(item, list):
            for secondary in item: # LLM had a tendency to return [[]]
                new_item = {}
                keys = list(secondary.keys())

                new_item["parameter"] = secondary[keys[0]]

                try:
                    float_number = float(secondary[keys[1]])
                    new_item["value"] = float_number
                except (ValueError, TypeError):
                    print("Could not convert string to float. Hence 0")
                    new_item["value"] = 0
                
                new_item["unit"] = secondary[keys[2]]

                new_result.append(new_item)
        else:
            
            new_item = {}
            keys = list(item.keys())

            new_item["parameter"] = item[keys[0]]

            try:
                float_number = float(item[keys[1]])
                new_item["value"] = float_number
            except (ValueError, TypeError):
                print("Could not convert string to float. Hence 0")
                new_item["value"] = 0
            
            new_item["unit"] = item[keys[2]]

            new_result.append(new_item)

    return new_result


def LLM_JSON_query(result):
    """
    Description:
        - Defining query to format text to json. 
    """
    query = f"""
        Given this text: [result]. Please alter it such that it fits a json format of a dictionary like this:
        [{{"parameter": "Iron", "value": 27, "unit": "umol/L"}}], but with different values
    """
    return query

def experiment1_main(file_name):
    """
    Description:
        - Experiment using phi3 to extract data line by line
    Input:
        - file_name
    Output:
        - List of dictionaries:  {"parameter":, "value":, "unit":}
    """
    content = x1_data()
    keywords = x1_keywords(content)

    file_path = file_name # TODO: change naming

    # find all relevant lines
    lines = extract_lines_from_unstructured(file_path, keywords)

    prompt = LLM_query(lines)

    text_result = ollama_phi3(prompt)

    text_result = text_result.split('\n')
    print(text_result)
    result = []
    for line in text_result:  # Attempting to load json line by line
        if line == '[' or line == ']':
            continue
        try:
            json_line = json.loads(line)
        except json.decoder.JSONDecodeError:
            continue
        result.append(json_line)

    abbr_result = all_abbr(result)
    
    json_result = standardise_result(abbr_result)
    
    return json_result

if __name__ == "__main__":
    print(experiment1_main('sample_data/0c848136-de54-49eb-a3c4-b04dda11ef42.txt') )
    #test_formatting()