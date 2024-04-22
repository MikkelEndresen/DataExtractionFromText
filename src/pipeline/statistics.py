from typing import List, Dict


def num_params_ext(params):
    '''
    Description:
        - Number of parameters extracted
    Input: 
        - List of dictionaries
    Output: 
        - Length of list
    '''
    return len(params)

def percentage_char_extracted(params: List[Dict[str, str]], text):
    '''
     Description:
        - Percentage of characters extracted from text file
    Input: 
        - List of dictionaries
        - Text object
    Output: 
        - Percentage value (numeric)
    '''

    chars_ext = 0
    for param in params:
        for key in param.keys():
            chars_ext += len(str(param[key])) # TODO: does this include "\n" etc. ?



