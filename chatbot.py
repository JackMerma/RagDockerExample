import os
from flask import Flask, request, jsonify
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
#from uuid import uuid4
from methods import *

app = Flask(__name__)

@app.route('/process_prompt', methods=['POST'])
def process_prompt():

    # Getting data
    data = request.get_json()
    query = data.get("query", "")
    entities = data.get("entities", [])
    ranking_number = data.get("ranking_number", "")

    if not query:
        return jsonify({"error": "No input provided"}), 400

    if not entities:
        return jsonify({"error": "No entities provided"}), 400

    if not ranking_number:
        return jsonify({"error": "No ranking number provided"}), 400

    # Casting ranking number to int
    ranking_number = min(int(ranking_number), len(entities))

    # Getting embedding model
    em_model = OllamaEmbeddings(model="nomic-embed-text")

    # Getting chunks
    #docs = get_docs(entities)
    documents = []
    loader = TextLoader("sample_text.txt")
    file_docs = loader.load()
    
    for doc in file_docs:
        documents.append(doc)

    text_splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=2)
    docs = text_splitter.split_documents(documents)
    #uuids = [str(uuid4()) for _ in range(len(docs))]

    # Defining vector store
    vector_store = Chroma.from_documents(
            docs,
            em_model,
            )

    # Retrieve relevant documents
    retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k":ranking_number, "score_threshold":0.1}
            )

    relevant_docs = retriever.invoke(query)
    relevant_contents = [doc.page_content for doc in relevant_docs]

    return jsonify({"retriever": relevant_contents})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
