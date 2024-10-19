import os
from langchain_community.chat_models.ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_chatbot.templates import get_messages


def build_response(topic, additional_info, query, history):

    # Building prompt
    messages = get_messages(history, query)
    prompt_template = ChatPromptTemplate.from_messages(messages)
    prompt = prompt_template.invoke({"topic": topic, "additional_info": additional_info})
    
    # Getting model
    llm_model = ChatOllama(base_url=os.getenv('OLLAMA_URL'), model=os.getenv('LLM_MODEL'), temperature=0.0)

    # Returning reponse
    return llm_model.invoke(prompt)
