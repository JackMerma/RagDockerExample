def get_docs(entities):

    docs = []

    for entity in entities:
        docs.append(entity.get("content", ""))

    return docs
