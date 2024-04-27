import json

def x1_data():
    """
    Description:
        - Return raw json data from X1 file
    Output:
        - List of dictionaries
    """

    x1 = open('pipeline/X1.json', 'r')
    content = json.load(x1)

    return content

def x1_keywords(content):
    """
    Description:
        - Returns all the key words, abbrevetions and synonyms
    Input:
        - x1 list of dictionaries
    Output:
        - All keywords
    """

    all_keywords = []
    for parameter in content:
        all_keywords.append(parameter['Abbreviation'].lower())
        for synonym in parameter['Synonyms']:
            all_keywords.append(synonym.lower())
    
    return all_keywords

def extract_lines_from_unstructured(file_path, all_keywords):
    """
    Description:
        - Finds all relevant lines in document
    Input:
        - file_path
        - x1 keywords
    Output:
        - List of dictionaries: {parameter_name: line}
    """
    file = open(file_path, 'r')
    data = file.read()    

    lines = data.split('\n')

    found = {}
    for i, line in enumerate(lines):
        for word in line.split():
            if word.lower() in all_keywords:
                found[word] = line

    return  found