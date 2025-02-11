from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from auth import register_user, login_user
from config import Config
import os

app = Flask(__name__)
CORS(app)

# Use config for settings
OLLAMA_API = Config.OLLAMA_API
PORT = Config.PORT

# Serve static files
@app.route('/')
def root():
    try:
        return send_from_directory('static', 'login.html')
    except Exception as e:
        print(f"Error serving login.html: {str(e)}")
        return f"Error: {str(e)}", 404

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    response, status_code = register_user(
        data.get('name'),
        data.get('username'),
        data.get('password'),
        data.get('email'),
        data.get('location')
    )
    return jsonify(response), status_code

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    response, status_code = login_user(
        data.get('username'),
        data.get('password')
    )
    return jsonify(response), status_code

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        
        print(f"Sending request to Ollama with message: {message}")
        
        # Cloud-optimized model settings
        response = requests.post(OLLAMA_API, json={
            "model": "mistral:7b-instruct-v0.2-q4_K_M",
            "prompt": message,
            "stream": False,
            "options": {
                "num_thread": Config.NUM_THREADS,
                "num_ctx": Config.CONTEXT_SIZE
            }
        })
        
        # Print the raw response for debugging
        print(f"Ollama response status: {response.status_code}")
        print(f"Ollama response content: {response.text}")
        
        if response.status_code == 200:
            return jsonify({
                "response": response.json()["response"]
            })
        else:
            # More detailed error logging
            error_message = response.text.lower()
            print(f"Error from Ollama: {error_message}")
            
            if any(phrase in error_message for phrase in ["disk space", "not enough space"]):
                return jsonify({
                    "error": "Insufficient disk space. Please free up some space and try again."
                }), 507
            elif "model not found" in error_message:
                return jsonify({
                    "error": "Model mistral:7b-instruct-v0.2-q4_K_M not found. Please check if the model is properly installed."
                }), 404
            
            return jsonify({
                "error": f"Failed to get response from Ollama: {response.text}"
            }), 500
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Detailed error logging
        error_message = str(e).lower()
        if any(phrase in error_message for phrase in ["disk space", "not enough space"]):
            return jsonify({
                "error": "Insufficient disk space. Please free up some space and try again."
            }), 507
        
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=Config.DEBUG) 