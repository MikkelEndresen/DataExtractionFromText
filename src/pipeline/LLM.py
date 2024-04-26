

from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM

def setup_Llama3():

    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

    tokenizer.save_pretrained('Model/')
    model.save_pretrained('Model/')

def load_model():

    #setup_Llama3()

    tokenizer = AutoTokenizer.from_pretrained('Model/')
    model = AutoModel.from_pretrained('Model/')

    return tokenizer, model


from transformers import pipeline

from transformers import GPTNeoForCausalLM, GPT2Tokenizer
def neo():

    model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
    tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")

    prompt = (
        "In a shocking finding, scientists discovered a herd of unicorns living in a remote, "
        "previously unexplored valley, in the Andes Mountains. Even more surprising to the "
        "researchers was the fact that the unicorns spoke perfect English."
    )

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    gen_tokens = model.generate(
        input_ids,
        do_sample=True,
        temperature=0.9,
        max_length=100,
    )
    gen_text = tokenizer.batch_decode(gen_tokens)[0]

from langchain_community.llms import Ollama

def ollama_phi3(query):
    """
    Setup: 
        - Ollama pull phi3
    """

    llm = Ollama(model='phi3')
    result = llm.invoke (query)
    
    return result

if __name__ == "__main__":
    ollama_phi3
   
    # model, tokenizer = load_model()

    # print("second stage")
    # transcriber = pipeline(model=model)

    # print("third stage")
    # print(transcriber("List all numbers between 1 and 10."))
    
    # print("complete")