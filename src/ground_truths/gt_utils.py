import json
from pipeline.utils import remove_duplicates, all_abbr

# Methods to clean gpt extracted parameters and values

def getX1Params():
    """
        Description:
            Extracts parameters from x1.json
        Output:
            A list of all abbr and synonyms.
    """
    x1 = open('pipeline/X1.json', 'r')
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

    # TODO: Partial Params.

    for dict in parameters:
        if dict['parameter'].lower() in x1params:
            new_dict = {}
            new_dict['parameter'] = dict['parameter']

            try:
                value = float(dict['value'])
            except ValueError:
                value = 0
            new_dict['value'] = value

            new_dict['unit'] = dict['unit']

            aligned.append(new_dict)
    
    return aligned


def clean_ground_truths(file_name):
    """
        Description:
           Cleans up the gpt ground truths and creates new files for the ground thruths
        Input:
            - Sample_data file name
        Output:
            - Dictionary of ground truths
    """

    path_to_file = 'ground_truths/gpt_gt/gpt_gt_' + file_name + '.json'
    file = open(path_to_file, 'r')
    gpt_gt = json.load(file)

    print(f"Initial num params: {len(gpt_gt)}")

    aligned = check_X1alignement(gpt_gt)

    abbr = all_abbr(aligned)

    no_duplicates = remove_duplicates(abbr)

    return no_duplicates