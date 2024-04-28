#import pytest
import os
import time
from datetime import datetime
import csv

#import sys
#sys.path.append('../pipeline')
#from pipeline import pipeline
#sys.path.append('../pipeline/statistics')
from pipeline import pipeline
from pipeline.statistics import percentage_char_extracted, num_params_ext, calculate_accuracy
from pipeline.experiment1 import experiment1_main
from pipeline.experiment2 import experiment2_main
from ground_truths.gt_utils import clean_ground_truths

'''
What information should be stored results.csv?
    - Date
    - Stats
        - Runtime
        - Num parameters extracted
        - Character percentage
        - Accuracy (N.A.) for now 
    - Resulting list
'''

def test_pipeline_stats():
    
    # loop through each file in the folder
    directory = 'sample_data/'
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            # calculate runtime
            start_time = time.time()

            result = experiment2_main(path)

            end_time = time.time()
            runtime = end_time - start_time

            # perform the various stats
            f = open(path, 'r')
            content = f.read() 
            current_datetime = datetime.now()
            percentage = percentage_char_extracted(result, content)
            num_params = num_params_ext(result)
            accuracy = calculate_accuracy(result, filename)

            ## Get ground truth
            file_name = filename[:-4]
            ground_truth = clean_ground_truths(file_name)

            # save into dictionary
            data = {
                'Experiment': 'experiment2_4', ### TODO: Change
                'DateTime': current_datetime,
                'FileName': filename,
                'Percentage': percentage,
                'Num Parameters Extracted': num_params,
                'Accuracy': accuracy,
                'Runtime': runtime, 
                'Result': result,
                'Ground Truth': ground_truth
            }

            print('-'*80)
            print(f"This is the data: {data}")

            csv_file = 'results.csv'
            results_csv = open(csv_file, 'a', newline='')
            header_fields = list(data.keys())
            writer = csv.DictWriter(results_csv, fieldnames=header_fields)

            #Write header if file is empty
            if os.stat(csv_file).st_size == 0:
                writer.writeheader()
            
            writer.writerow(data)

if __name__ == "__main__":
    test_pipeline_stats()
