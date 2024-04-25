

from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM

def setup_Llama3():

    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")

    tokenizer.save_pretrained('Model/')
    model.save_pretrained('Model/')

def load_model():

    setup_Llama3()

    tokenizer = AutoTokenizer.from_pretrained('Model/')
    model = AutoModel.from_pretrained('Model/')

    return tokenizer, model


from transformers import pipeline

if __name__ == "__main__":
    print("first stage")
    model, tokenizer = load_model()

    print("second stage")
    transcriber = pipeline(model=model)

    print("third stage")
    print(transcriber("List all numbers between 1 and 10."))
    
    print("complete")