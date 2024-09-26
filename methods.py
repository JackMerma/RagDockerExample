from langchain_core.documents import Document

def get_docs(entities):

    documents = []

    for entity in entities:
        doc = Document(
                page_content=entity.get("content", ""),
                metadata={"id": entity.get("id", "")}
                )
        documents.append(doc)

    return documents
