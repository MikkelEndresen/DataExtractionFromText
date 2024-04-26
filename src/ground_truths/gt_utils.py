import json

def getX1Params():
    x1 = open('../pipeline/X1.json', 'r')
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

    x1params = getX1Params()
    
    aligned = []

    # TODO: Partial match. E.g. "R U-Creatinine"

    for dict in parameters:
        if dict['parameter'].lower() in x1params:
            aligned.append(dict)
    
    return aligned


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
    print(f"Number of paramaters before removing duplicates: {len(parameters)}")
    no_duplicates = []

    for item in parameters[::-1]:
        check = True
        for duplicate in no_duplicates:
            if duplicate['parameter'].lower() == item['parameter'].lower():
                check = False
                print(f"Duplicate removed: {duplicate}")
        if check:
            no_duplicates.append(item)

    print(f"Number of paramaters after removing duplicates: {len(no_duplicates)}")

    return no_duplicates


def clean_ground_truths(file_name):
    """
        Description:
           Cleans up the gpt ground truths and creates new files for the ground thruths
        Input:
            - Sample_data file name
        Output:
            - Dictionary of ground truths
    """

    path_to_file = 'gpt_gt/gpt_gt_' + file_name + '.json'
    file = open(path_to_file, 'r')
    gpt_gt = json.load(file)

    print(f"Initial num params: {len(gpt_gt)}")

    aligned = check_X1alignement(gpt_gt)

    print(f"Aligned num params: {len(aligned)}")

    no_duplicates = remove_duplicates(aligned)

    # TODO: Error/Standardise 'Value' missing/wrong format

    return no_duplicates

if __name__ == "__main__":
    clean_ground_truths("0b8706dc-c9af-4c6b-887d-2f85b5a511e7")