# Rule based approach
from pipeline.utils import x1_data, x1_keywords,  extract_lines_from_unstructured, remove_duplicates
from pipeline.utils import find_numeric, find_unit, all_abbr


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
        entry['value'] = find_numeric(lines[line]) # find numeric on the line
        entry['unit'] = find_unit(lines[line])     # find the unit descirptor


        result.append(entry)

    result = all_abbr(result) # paramater names to abbr.
    
    result = remove_duplicates(result)

    return result

if __name__ == "__main__":
    experiment2_main('sample_data/0c848136-de54-49eb-a3c4-b04dda11ef42.txt')  # test