from jsonformer import Jsonformer
from transformers import AutoModelForCausalLM, AutoTokenizer

from pipeline.utils import x1_data, x1_keywords,  extract_lines_from_unstructured, all_abbr

import json


def setup_phi():
    
    directory_path = "phi/"

    # Directory to save the model and tokenizer
    # Create the directory if it doesn't exist
    import os
    if not os.path.exists(directory_path):

        os.makedirs(directory_path)

        # download models
        tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)

        # Save the model and tokenizer
        model.save_pretrained(directory_path)
        tokenizer.save_pretrained(directory_path)
    else:
        # Load the model and tokenizer from the saved directory
        model = AutoModelForCausalLM.from_pretrained(directory_path, trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(directory_path, trust_remote_code=True)

    return model, tokenizer

def jsonformer_test():
   

    json_schema = {
        "type": "object",
        "properties": {
            "parameter": {"type": "string"},
            "value":{"type": "number"},
            "unit": {"type": "string"}
        }
    }

    model, tokenizer = setup_phi()

    prompt = "Extract the lab report data that fit the given schema."

    
    jsonformer = Jsonformer(model, tokenizer, json_schema, prompt)
    generated_data = jsonformer()

    print(generated_data)

    print(json.loads(generated_data))


#### Try Langchain: JsonOutPutPArser

if __name__ == "__main__":
    jsonformer_test()
    # print(experiment1_main('sample_data/0c848136-de54-49eb-a3c4-b04dda11ef42.txt') )
