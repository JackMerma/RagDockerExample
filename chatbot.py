from flask import Flask, request, jsonify
from langchain_community.chat_models.ollama import ChatOllama

app = Flask(__name__)

@app.route('/process_prompt', methods=['POST'])
def process_prompt():

    # Getting data
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 404


    # Execute the model
    try:
        model = ChatOllama(model="gemma:2b", temperature=0, base_url="http://ollama:11434")
        response = model.invoke(prompt)
        result = response.content.strip()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Returning the answer in JSON format
    return jsonify({"response": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


