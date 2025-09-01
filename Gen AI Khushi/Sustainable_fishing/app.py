from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

PERPLEXITY_API_KEY = "Your_key"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code == 200:
            resp_json = r.json()
            text = resp_json['choices'][0]['message']['content']
            return jsonify({"text": text})
        else:
            return jsonify({"text": f"Error from Perplexity API: {r.status_code}, {r.text}"}), 500
    except Exception as e:
        return jsonify({"text": f"Request failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
