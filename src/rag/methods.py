import os
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


def create_docs(entities):

    documents = []

    for entity in entities:
        doc = Document(
                page_content=entity.get("content", ""),
                metadata={"id": entity.get("id", "")}
                )
        documents.append(doc)

    return documents

def handler_ranking_number(ranking_number, entities_len):

    ranking_number = min(ranking_number, entities_len)
    ranking_number = 1 if ranking_number < 1 else ranking_number


def retriever_content(docs):

    relevant_contents = []

    for doc in docs:
        content = doc.page_content
        doc_id = doc.metadata["id"]

        relevant_contents.append({
            "id": doc_id,
            "content": content
            })

    return relevant_contents


def build_retriever(query, entities, ranking_number):

    # Getting docs
    documents = create_docs(entities)

    # Defining the embedding model
    embedding_model =  OllamaEmbeddings(
            model=os.getenv('EMBEDDING_MODEL'),
            base_url=os.getenv('OLLAMA_URL')
            )

    # Creating a vector store
    vector_store =  Chroma.from_documents(
            documents,
            embedding_model
            )

    # Retrieve relevant docs
    retriever =  vector_store.as_retriever(
            search_type=os.getenv('RETRIEVER_SEARCH_TYPE'),
            search_kwargs={"k":ranking_number, "score_threshold": 0.1}
            )
    return retriever.invoke(query)
