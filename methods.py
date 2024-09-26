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


def handler_ranking_numer(ranking_number, entities_len):

    ranking_number = min(ranking_number, entities_len)
    ranking_number = 1 if ranking_number < 1 else ranking_number


def get_retriever_content(docs):

    relevant_contents = []

    for doc in docs:
        content = doc.page_content
        doc_id = doc.metadata["id"]

        relevant_contents.append({
            "id": doc_id,
            "content": content
            })

    return relevant_contents
