from pipeline.utils import x1_data, x1_keywords,  extract_lines_from_unstructured
from pipeline.LLM import ollama_phi3
import json

def LLM_query(lines):
    query = f"""
    Context: You are a medical expert specializing in extracting structured data from lab reports.
    Task: For each entry in the 
        - The value of "parameter" in the template should be equal to the key in the dictionary.
        - The value of "value" should be a numeric value extracted from the value in the dictionary.
        - The value of "unit" should be the unit of measurement for the parameter, also in the value in the dictionary.

    Refer to the Example to see the input-output relationship. All output should be in JSON format of a list of dictionaries.
    Ensure all values are represented as strings with double quotations. 

    Examples:
        Input [{{"Total Testosterone": "Total Testosterone (Siemens) 39.2 nmol/L (8.3-29)"}}, {{"Iron (10-30) umol/L 40 33 21 27"}}]
        Output: [{{"parameter": "Total Testosterone", "value": 39.2, "unit": "nmol/L"}}, {{"parameter": "Iron", "value": 27, "unit": "umol/L"}}]

    Dictionary: {lines}

    Template: [{{"parameter": , "value": , "unit": }}]
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
            for secondary in item:
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

    query = f"""
        Given this text: [result]. Please alter it such that it fits a json format of a dictionary like this:
        [{{"parameter": "Iron", "value": 27, "unit": "umol/L"}}], but with different values
    """
    return query

def experiment1_main(file_name):
    """
    Description:
        - 
    Input:
        - file_name
    Output:
        - List of dictionaries:  {"parameter":, "value":, "unit":}
    """
    content = x1_data()
    keywords = x1_keywords(content)

    file_path = file_name # TODO: change naming

    # find all relevant lines
    lines =  extract_lines_from_unstructured(file_path, keywords)

    # remove duplicates, and set keys to Abbr
    final_lines = {}
    for key in lines.keys():
        for x in content:
            lowercase_synonyms = [item.lower() for item in x['Synonyms']]
            if key.lower() == x['Abbreviation'].lower() or key.lower() in lowercase_synonyms:
                final_lines[x['Abbreviation']] = lines[key]

    prompt = LLM_query(final_lines)

    text_result = ollama_phi3(prompt)
    #print(text_result)

    #print('-'*80)
    #print(f"Plain text: {text_result}")

    text_result = text_result.split('\n')

    json_result = []
    for line in text_result:
        #print(line)
        if line == '[' or line == ']':
            continue
        try:
            json_line = json.loads(line)
            #print(f"Json line: {json_line}")
        except json.decoder.JSONDecodeError:
            # try: 
            #     new_line = ollama_phi3(LLM_JSON_query(line))
            #     json_line = json.loads(new_line)
            # except json.decoder.JSONDecodeError:
            #     continue
            continue
        json_result.append(json_line)

    #print(f"Json Result: {json_result}")
    json_result =  standardise_result(json_result)

    # print(f"Result: {json_result}")
    # print(f"Type: type{json_result}")

    #json_result = json.loads(json_result)

    # Remove anything that is not json compatible?

    # TODO: convert line by line to improve retention
    

    # try: 
    #     json_result = json.loads(text_result)
    # except json.decoder.JSONDecodeError:
    #     try:
    #         json_result = ollama_phi3(LLM_JSON_query(text_result))
    #         json_result = json.loads(text_result)
    #     except json.decoder.JSONDecodeError:
    #         print("Unable to load json")
    #         json_result = []
    
    #json_result =  standardise_result(json_result)
    
    #print(f"Result: {json_result}")
    #print(f"Type: type{json_result}")

    
    return json_result

if __name__ == "__main__":
    experiment1_main('sample_data/0c848136-de54-49eb-a3c4-b04dda11ef42.txt')  
    #test_formatting()