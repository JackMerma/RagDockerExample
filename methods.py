from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

def get_docs(entities):

    docs = []

    for entity in entities:
        doc = Document(
                page_content=entity.get("content", ""),
                metadata={"id": entity.get("id", "")}
                )
        docs.append(doc)

    return docs
