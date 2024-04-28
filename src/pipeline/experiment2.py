# Rule based approach
from pipeline.utils import x1_data, x1_keywords,  extract_lines_from_unstructured, remove_duplicates
from pipeline.utils import find_numeric, find_unit


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