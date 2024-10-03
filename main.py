import os
from flask import Flask, request, jsonify
from rag.methods import *

# Global variables
app = Flask(__name__)
OLLAMA_URL = os.getenv('OLLAMA_URL')


@app.errorhandler(Exception)
def handle_exception(error):
    response = {
            "error": str(error)
            }
    return jsonify(response), 400


@app.route('/rag', methods=['POST'])
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
    embedding_model = get_embedding_model(OLLAMA_URL)
    vector_store = get_vector_store(documents, embedding_model)

    # Retrieve relevant docs
    retriever = get_retriever(vector_store, ranking_number)
    relevant_docs = retriever.invoke(query)
    relevant_contents = get_retriever_content(relevant_docs)

    return jsonify({"response": relevant_contents})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
