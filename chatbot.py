from langchain_community.chat_models.ollama import ChatOllama

model = ChatOllama(model="gemma:2b", temperature=0, base_url="http://ollama:11434")

response = model.invoke("Escribe algún poema de gongora")

with open ("output.log", "w") as file:
    file.write(response.content)
