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
        print(f"This is a line: {line}")

        # Ab. Antibodies
        # -, remove or not

        words = line.split()
        # one word
        for word in words:
            if word.lower() in all_keywords:
                print(f"word found: {word}")
                found[word] = line

            # change words to fit X1.json
            if word == "Ab.":
                word = "Antibodies"
        
        # two word
        for i in range(len(words)-1):
            two_word = words[i] + " " + words[i+1]
            if two_word in all_keywords:
                print(f"New word found: {two_word}")
                found[two_word] = line

        # three word
        for i in range(len(words)-2):
            three_word = words[i] + " " + words[i+1] + " " + words[i+2]
            if three_word in all_keywords:
                print(f"New word found: {three_word }")
                found[three_word ] = line

    return  found

def find_numeric(line):
    words = line.split(' ')

    numeric = []
        
    for word in words:
        try:
            num = float(word)
        except ValueError:
            continue
        numeric.append(num)

    if len(numeric) > 0:
        return numeric[-1]
    return 0

def find_unit(line):
    units_of_measurement = [
    "g/L", "mg/dL", "ug/L", "mmol/L", "pmol/L", "nmol/L", "mmol/L",  # Mass Concentration Units
    "x10^9/L", "x10^12/L", "x10^6/L",  # Count Units
    "%",  # Percentage
    "U/L", "mm/h", "mL/min/1.73m²",  # Rate or Activity Units
    "pH", "IU/L", "umol/L", "mIU/L"  # Other Units
    ]

    unit = ""

    words = line.split(' ')
    for word in words:
        if word in units_of_measurement:
            unit = word
    
    return unit

def remove_duplicates(parameters):
    """
        Description:
           Removes duplicates, based on 'parameter' from a list of dicts. 
           Assuming latest recorded value is last in the list.
        Input:
            List of dictionaries: {'parameter':, 'value', 'unit': }
        Output:
            List of dictionaries: {'parameter':, 'value', 'unit': }
    """


    # Find all the the duplicates and add them to a dictionary.
        # then loop through the values of that dictionary and and either
        # take the latest, all the one with legit values
    
    # add them all to a dict

    # #TODO: make sure paramater = abbr

    paramaters_dict = {}
    for item in parameters[::-1]:
        param = item['parameter'].lower()
        if param in list(paramaters_dict.keys()):
            paramaters_dict[param.lower()].append(item)
        else:  
            paramaters_dict[param.lower()] = [item]
            

    print(f"Paramater dict: {paramaters_dict}")

    no_duplicates = []

    for param in paramaters_dict.keys():
        if len(paramaters_dict[param]) > 1:
            # remove based on value and unit validity
            # if equal
            score = []
            for entry in paramaters_dict[param]:
                int_score = 0
                if entry['value'] != 0:
                    int_score += 1
                if entry['unit'] != '':
                    int_score += 1
                score.append(int_score)
            
            max_index = score.index(max(score)) # returns the index of the highest score
                                                # or the first highest, which is the most
                                                # recent value
            
            no_duplicates.append(paramaters_dict[param][max_index])
            
        else:
            no_duplicates.append(paramaters_dict[param][0])

    print(f"Length of no duplicates: {len(no_duplicates)}")
    print(f"Initial length: {len(parameters)}")

    return no_duplicates

