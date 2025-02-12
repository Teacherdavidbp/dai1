from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from auth import register_user, login_user
from config import Config
import os

app = Flask(__name__)
CORS(app, origins=[
    "https://dai1.netlify.app",  # Your actual Netlify URL
    "http://localhost:3000",
    "http://localhost:5000"
], supports_credentials=True)

# Use config for settings
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
        
        print(f"Sending request to DeepSeek with message: {message}")
        
        headers = {
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json={
                "model": Config.DEEPSEEK_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
                ]
            }
        )
        
        if response.status_code == 200:
            return jsonify({
                "response": response.json()["choices"][0]["message"]["content"]
            })
        else:
            return jsonify({
                "error": f"API Error: {response.text}"
            }), response.status_code
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test_connection():
    return jsonify({
        "status": "success",
        "message": "Backend is connected!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=Config.DEBUG) 