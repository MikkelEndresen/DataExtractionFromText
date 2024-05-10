from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
import os

import json
import re

from pipeline.utils import x1_data, x1_keywords,  extract_lines_from_unstructured

from ground_truths.gt_utils import check_X1alignement

def standardise_result(result):
    """
    Description:
        - Making sure there are no key errors. 
    Input:
        - result list of dictionaries
    Output:
        - List of dictionaries:  {"parameter":, "value":, "unit":}
    """

    new_result = []

    for item in result:

        if isinstance(item, list):
            for secondary in item: # LLM had a tendency to return [[]]
                new_item = {}
                keys = list(secondary.keys())

                new_item["parameter"] = secondary[keys[0]] # TODO: Make sure this is abbreviation                

                try:
                    num = ''.join(filter(lambda x: x.isdigit() or x == '.',  item[keys[1]]))
                    #num = re.sub(r'[^\d.]*([\d.]+)[^\d.]*', r'\1', item[keys[1]])
                    float_number = float(num)
                    new_item["value"] = float_number
                except (ValueError, TypeError):
                    #print("Could not convert string to float. Hence 0")
                    new_item["value"] = 0
                
                if secondary[keys[2]] is None:
                    new_item["unit"] = "None"
                else:
                    new_item["unit"] = secondary[keys[2]]

                new_result.append(new_item)
        else:
            
            new_item = {}
            keys = list(item.keys())

            new_item["parameter"] = item[keys[0]]

            try:   
                num = ''.join(filter(lambda x: x.isdigit() or x == '.',  item[keys[1]]))
                #num = re.sub(r'[^\d.]*([\d.]+)[^\d.]*', r'\1', item[keys[1]])
                float_number = float(num)
                new_item["value"] = float_number
            except (ValueError, TypeError):
                #print("Could not convert string to float. Hence 0")
                new_item["value"] = 0
            
            if item[keys[2]] is None:
                new_item["unit"] = "None"
            else:
                new_item["unit"] = item[keys[2]]

            new_result.append(new_item)

    return new_result


def experiment4_main(file_path):

    GOOGLE_API_KEY = 'AIzaSyDWNP5-fhmYfjzMdN-_a3gV7-j4bnm8xpg'

    if 'GOOGLE_API_KEY' in os.environ:
        print(f"The environment variable GOOGLE_API_KEY exists with value: {os.environ['GOOGLE_API_KEY']}")
    else:
        os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
        print(f"Succesfully set the GOOGLE_API_KEY")

    #genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

    model = ChatGoogleGenerativeAI(model="gemini-pro")

    class Pipeline(BaseModel):
        parameter: str = Field(description="Name of analytes, e.g. HBA1", max_length=20)
        value: str = Field(description="Value of analytes, e.g. 10.2", max_length=10)
        unit: str = Field(description="Unit the value is measured in, e.g. mmol/L", max_length=10)

    content = x1_data()
    keywords = x1_keywords(content)


    # find all relevant lines
    lines = extract_lines_from_unstructured(file_path, keywords)

    # And a query intented to prompt a language model to populate the data structure.
    query = f"""
            From each of the following dictionaries value extract the paramater, value, and unit of the analyte.
            Dictionaries: [{lines}]
            Examples:
                Input: [{{"Total Testosterone": "Total Testosterone (Siemens) 39.2 nmol/L (8.3-29)"}}, {{"Iron": "Iron (10-30) umol/L 40 33 21 27"}}]
                Output: [{{"parameter": "Total Testosterone", "value": 39.2, "unit": "nmol/L"}}, {{"parameter": "Iron", "value": 27, "unit": "umol/L"}}]
    """

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Pipeline)

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    result = chain.invoke({"query": query})
    #print(result)
    if result is None:
        return [{'parameter': 'N.A.', 'value': 0, 'unit': 'N.A.'}]

    #TODO: remove duplicates

    try:
        standardised = standardise_result(result) 
    except AttributeError as e:
        #print(result)
        #print(e)
        return [{'parameter': 'N.A.', 'value': 0, 'unit': 'N.A.'}]
    #print(80*'-')
    #print(standardised)
    #print(80*'-')
    aligned = check_X1alignement(standardised) # standardise_result(result)

    #print(aligned)
    
    return aligned