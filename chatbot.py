import os
from flask import Flask, request, jsonify
import ollama
import chromadb
from methods import *
from llama_index.embeddings.ollama import OllamaEmbedding

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

    # Getting docs
    documents = get_docs(entities)
    client = chromadb.Client()
    collection = client.create_collection(name="docs")


    # Tutorial example https://docs.llamaindex.ai/en/stable/examples/embeddings/ollama_embedding/
    ollama_embedding = OllamaEmbedding(
            model_name="gemma:2b",
            base_url=OLLAMA_URL,
            )

    pass_embedding = ollama_embedding.get_text_embedding_batch(
            ["This is a passage!", "This is another passage"], show_progress=True
            )

    query_embedding = ollama_embedding.get_query_embedding("Where is blue?")

    relevant_contents = "reponse OK"

    return jsonify({"retriever": relevant_contents})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
