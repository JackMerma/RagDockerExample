import os
from flask import Flask, request, jsonify
from rag.methods import handler_ranking_number, build_retriever, retriever_content
from langchain_chatbot.controller import build_response
from flask_swagger_ui import get_swaggerui_blueprint

# Global variables
app = Flask(__name__)
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://petstore.swagger.io/v2/swagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

"""
@app.errorhandler(Exception)
def handle_exception(error):
    response = {
            "error": str(error)
            }
    return jsonify(response), 400
"""


@app.route('/rag', methods=['POST'])
def rag():

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
    handler_ranking_number(ranking_number, len(entities))

    # Retrieve relevant docs
    relevant_docs = build_retriever(query, entities, ranking_number)
    relevant_contents = retriever_content(relevant_docs)

    return jsonify({"response": relevant_contents})


@app.route('/langchain', methods=['POST'])
def langchain():

    # Getting data
    data = request.get_json()
    query = data.get("query", "")
    topic = data.get("topic", "")
    additional_info = data.get("additional_info", "")
    history = data.get("history", [])

    # Asserting inputs
    if not query: raise Exception("No query provided")
    if not topic: raise Exception("No topic provided")
    if not additional_info: raise Exception("No additional information provided")

    # Processing
    response = build_response(topic, additional_info, query, history)
    return jsonify({"response": response.content})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
