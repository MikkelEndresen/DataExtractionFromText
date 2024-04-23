import pytest
import os
import time
from datetime import datetime
import csv

import sys
sys.path.append('../pipeline')
from pipeline import pipeline
from pipeline.statistics import percentage_char_extracted, num_params_ext

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
    directory = '../sample_data/'
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            # calculate runtime
            start_time = time.time()

            result = pipeline.pipeline(path)

            end_time = time.time()
            runtime = end_time - start_time

            # perform the various stats
            f = open(path, 'r')
            content = f.read() 
            current_datetime = datetime.now()
            percentage = percentage_char_extracted(result, content)
            num_params = num_params_ext(result)
            accuracy = None
            # save into dictionary
            data = {
                'DateTime': current_datetime, 
                'Percentage': percentage,
                'Num Parameters Extracted': num_params,
                'Accuracy': accuracy, 
                'Result': result
            }
            
            csv_file = 'results.csv'
            results_csv = open(csv_file, 'a', newline='')
            header_fields = ['DateTime', 'Percentage', 'Num Parameters Extracted', 'Accuracy', 'Result']
            writer = csv.DictWriter(results_csv, fieldnames=header_fields)

            # Write header if file is empty
            if os.stat(csv_file).st_size == 0:
                writer.writeheader()
            
            writer.writerow(data)

            assert content
            assert result
            assert num_params
            assert accuracy == None #TODO
