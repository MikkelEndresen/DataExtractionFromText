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
    #print(f"FileName: {file_name}")

    file_name = file_name[:-4]
    ground_truth = clean_ground_truths(file_name)

    correct = 0
    for item in result: 
        for truth in ground_truth:
            

            if truth['parameter'].lower() == item['parameter'].lower():
                correct += 1

                #print(f"Truth: {truth}")
               # print(f"Guess: {item}")

                try:
                    if float(truth['value']) == float(item['value']):
                        correct += 1
                        #print(f"This is the truth value: {truth['value']}, this is the found: {item['value']}")
                except (ValueError, TypeError) as e:
                    print(e)
                    print(item['value'])
                try:
                    if truth['unit'].lower() == item['unit'].lower():
                       # print(f"This is the truth unit: {truth['unit']}, this is the found: {item['unit']}")
                        correct += 1
                except AttributeError as e:
                    print(e)
                    print(item['unit'])
    if correct != 0:
       # print(f"Score: {correct / (len(ground_truth)*3)}")
        return correct / (len(ground_truth) * 3)
    return 0


if __name__ == "__main__":

    filename = '0c59298d-4205-4f6a-8bc9-c078123da03a.txt'
    file_name = filename[:-4]
    result = clean_ground_truths(file_name)

    print(f"Initial result: {result}")

    print(calculate_accuracy(result, filename))