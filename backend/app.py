from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Replace with the public IP address of the GPU instance
GPU_SERVER_URL = "http://213.181.122.2:43535/chat"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        logging.debug(f"Sending request to GPU server: {GPU_SERVER_URL} with message: {user_input}")
        response = requests.post(GPU_SERVER_URL, json={"message": user_input})
        response.raise_for_status()
        data = response.json()
        logging.debug(f"Received response from GPU server: {data}")
        response_text = data.get("response", "")
        retriever_info = data.get("retriever", [])

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return jsonify({"error": str(http_err)}), 500
    except Exception as e:
        logging.error(f"Other error occurred: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"response": response_text, "retriever": retriever_info})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
