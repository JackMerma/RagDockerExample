import os
from flask import Flask, request, jsonify
import chromadb
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from methods import *

app = Flask(__name__)
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama:11434')

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
    ranking_number = 1 if ranking_number < 1 else ranking_number

    # Getting docs
    documents = get_docs(entities)

    # Defining the embedding model
    embedding_model = OllamaEmbeddings(
            model="nomic-embed-text:latest",
            base_url=OLLAMA_URL
            )

    vector_store = Chroma.from_documents(
            documents,
            embedding_model
            )

    # Retrieve relevant docs
    retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k":ranking_number, "score_threshold": 0.1}
            )

    relevant_docs = retriever.invoke(query)

    relevant_contents = []

    for doc in relevant_docs:
        content = doc.page_content
        doc_id = doc.metadata["id"]

        relevant_contents.append({
            "id": doc_id,
            "content": content
            })

    return jsonify({"retriever": relevant_contents})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
