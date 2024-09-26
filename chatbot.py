import os
from flask import Flask, request, jsonify
import chromadb
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from methods import *

app = Flask(__name__)
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama:11434')

@app.errorhandler(Exception)
def handle_exception(error):
    response = {
            "error": str(error)
            }
    return jsonify(response), 400


@app.route('/process_prompt', methods=['POST'])
def process_prompt():

    ##########
    # INPUTS #
    ##########

    # Getting data
    data = request.get_json()
    query = data.get("query", "")
    entities = data.get("entities", [])
    ranking_number = data.get("ranking_number", "")

    # asserting inputs
    if not query: raise Exception("No query provided")
    if not entities: raise Exception("No entities provided")
    if not ranking_number: raise Exception("No ranking number provided")

    # Handling ranking number value
    try: ranking_number = int(ranking_number)
    except Exception as e: ranking_number = 1 # Default value
    handler_ranking_numer(ranking_number, len(entities))

    ##############
    # PROCESSING #
    ##############

    # Getting docs
    documents = get_docs(entities)

    # Defining the embedding model
    embedding_model = OllamaEmbeddings(
            model="mxbai-embed-large",
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
    relevant_contents = get_retriever_content(relevant_docs)

    return jsonify({"response": relevant_contents})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
