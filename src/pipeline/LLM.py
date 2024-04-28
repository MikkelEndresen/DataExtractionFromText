
from langchain_community.llms import Ollama

def ollama_phi3(query):
    """
    Description:
        - Prompts phi3 (temperature=0.0)
    Setup: 
        - (If not already done) Ollama pull phi3
    Return:
        - Returns the LLM response
    """

    llm = Ollama(model='phi3', temperature=0.0) # temp defaults to 0.8
    result = llm.invoke(query)

    return result

