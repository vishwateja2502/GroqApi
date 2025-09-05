import os
from dotenv import load_dotenv   # add this
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
load_dotenv()
app = Flask(__name__)

# Initialize Groq client with just the API key
client = Groq(api_key=os.environ["GROQ_API_KEY"])

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
    import os
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port, debug=False)
