
def getX1Params():
    x1 = open('X1.json', 'r')
    content = json.load(x1)
    print(f"Number of parameters: {len(content)}")
    print()

    all_keywords = []
    for parameter in content:
        all_keywords.append(parameter['Abbreviation'].lower())
        for synonym in parameter['Synonyms']:
            all_keywords.append(synonym.lower())

    
    print(f"Number of keywords: {len(all_keywords)}")
    return all_keywords

def check_X1alignement(parameters):
    """
        Description:
            Checks a list of dictionary against the desired parameters in X1.json
        Input:
            List of dictionaries: {'parameter':, 'value', 'unit': }
        Output:
            List of dictionaries: {'parameter':, 'value', 'unit': }
    """

    