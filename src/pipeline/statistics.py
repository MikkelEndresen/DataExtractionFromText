from typing import List, Dict
import io


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

def percentage_char_extracted(params: List[Dict], file_obj: io.TextIOWrapper):
    '''
     Description:
        - Percentage of characters extracted from text file
    Input: 
        - List of dictionaries
        - Text object
    Output: 
        - Percentage value (numeric)
    '''

    chars_list = 0
    for param in params:
        for key in param.keys():
            chars_list += len(str(param[key])) # TODO: does this include "\n" etc. ?

    chars_file =  sum(1 for char in file_obj if char.strip())

    return round(chars_list / chars_file, 3)


