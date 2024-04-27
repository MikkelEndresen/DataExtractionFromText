from typing import List, Dict
import io
from ground_truths.gt_utils import clean_ground_truths

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


def calculate_accuracy(result, file_name):
    """
    Description:
        - Total num = len(ground_truth) * 3
        - Earn one for each of the three desire values correct.
    Input:
        - Output Dictionary
        - File name of ground truth
    Output:
        - Percentage value
    """


    file_name = file_name[:-4]
    ground_truth = clean_ground_truths(file_name)

    print('-'*80)
    print("This is the result: ")
    print(result)
    correct = 0
    for item in result: 
        print(item)
        for truth in ground_truth:
            if truth['parameter'].lower() == item['parameter'].lower():
                correct += 1
                if truth['value'] == item['value']:
                    correct += 1
                if truth['unit'].lower() == item['unit'].lower():
                    correct += 1
                
    if correct != 0:
        correct / (len(ground_truth) * 3)
    return 0