from langchain_community.chat_models.ollama import ChatOllama

model = ChatOllama(model="gemma:2b", temperature=0, base_url="http://ollama:11434")

response = model.invoke("Write a 'hello world' code in java")

with open ("log_result.txt", "w") as file:
    file.write(response.content)
