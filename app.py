import os
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq

app = Flask(__name__)

# Initialize Groq client with just the API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        response = chat_completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
