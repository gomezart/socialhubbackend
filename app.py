import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    scenario = data.get("scenario")

    if not message or not scenario:
        return jsonify({"error": "Message and scenario are required."}), 400

    # Define scenario-based system prompt
    system_prompts = {
        "dating": "You are a world-class AI dating coach. Provide insightful advice on dating, relationships, and attraction.",
        "networking": "You are a top networking expert. Give guidance on making professional connections, career networking, and effective communication.",
        "confidence": "You are a confidence-building expert. Help users overcome self-doubt, improve social skills, and develop a strong mindset."
    }

    system_prompt = system_prompts.get(scenario, "You are an AI assistant providing expert advice.")

    try:
        # Updated OpenAI API call (latest syntax)
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )

        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's port or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)

