# Rule based approach
from pipeline.utils import x1_data, x1_keywords,  extract_lines_from_unstructured
from ground_truths.gt_utils import remove_duplicates


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

def experiment2_main(file_name):

    content = x1_data()
    keywords = x1_keywords(content)

    file_path = file_name # TODO: change naming

    # find all relevant lines
    lines =  extract_lines_from_unstructured(file_path, keywords)

    result = []

    for line in lines:

        entry = {}

        entry['parameter'] = line
        entry['value'] = find_numeric(lines[line])
        entry['unit'] = find_unit(lines[line])


        result.append(entry)

    print(f"Result before removing duplicates: {result}")
    result = remove_duplicates(result)

    # Remove dupliactes. 
        # - Make sure to take the "best" version in case
        # the param name was mentinoed in some weird sentence
        # instead of with a value and unit. 
    print("After")
    print(result)
    return result

if __name__ == "__main__":
    experiment2_main('sample_data/0c848136-de54-49eb-a3c4-b04dda11ef42.txt')  