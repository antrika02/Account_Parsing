import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# The model and template variables
model = "llama3.1:latest"
system_prompt = '''
You are an intelligent Assistant.
Based On User Query, Provide Title, Description, and Tags For Youtube Video Upload.
Respond In JSON Format As Below JSON Structure Only:
{
  "title":"{title}",
  "description":"{description with hash tags}",
  "tags": "{tag1,tag2,tag3...}"
}
'''

@app.route('/generate', methods=['POST'])
def generate():
    # Extracting the prompt from the request
    user_prompt = request.json.get("prompt", "")

    # The API request payload
    data = {
        "system": system_prompt,
        "prompt": user_prompt,
        "model": model,
        "format": "json",
        "stream": False,
        "options": {"temperature": 2.5, "top_p": 0.99, "top_k": 100,"max_tokens": 1000},
    }

    # Sending request to the external API to generate the response
    response = requests.post("http://localhost:11434/api/generate", json=data, stream=False)

    if response.status_code == 200:
        try:
            json_data = json.loads(response.text)
            generated_response = json.loads(json_data["response"])
            return jsonify(generated_response), 200

        except json.JSONDecodeError:
            return jsonify({"error": "Error parsing response from model."}), 500
    else:
        return jsonify({"error": f"Failed to connect to model API. Status code: {response.status_code}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5227, debug=True)

