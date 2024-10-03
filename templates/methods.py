import os
from langchain_community.chat_models.ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate


def get_llm_model():

    ollama_url = os.getenv('OLLAMA_URL')
    return ChatOllama(base_url=ollama_url, model=os.getenv('LLM_MODEL'), temperature=0.0)


def get_template_from_messages():

    messages = [
            ("system", os.getenv('INITIAL_SYSTEM_MESSAGE')),
            ("human", os.getenv('INITIAL_USER_MESSAGE'))
            ]

    return messages


def get_model_response(programming_language, topic):

    prompt_template = ChatPromptTemplate.from_messages(get_template_from_messages())
    prompt = prompt_template.invoke({"programming_language": programming_language, "topic": topic})
    
    # Getting model
    llm_model = get_llm_model()

    # Returning reponse
    return llm_model.invoke(prompt)
