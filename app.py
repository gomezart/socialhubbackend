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

# Store chat history per user (basic version)
conversation_history = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    scenario = data.get("scenario")

    if not message or not scenario:
        return jsonify({"error": "Message and scenario are required."}), 400

    # Define scenario-based system prompt
    system_prompts = {
        "dating": "You are a world-class AI dating coach. Provide insightful advice on dating, relationships, and attraction. Always ask open-ended questions to keep the conversation going.",
        "networking": "You are a top networking expert. Give guidance on making professional connections, career networking, and effective communication. Engage users by asking questions.",
        "confidence": "You are a confidence-building expert. Help users overcome self-doubt, improve social skills, and develop a strong mindset. Encourage responses and personal reflections."
    }

    system_prompt = system_prompts.get(scenario, "You are an AI assistant providing expert advice.")

    # Store conversation per session (basic)
    session_id = "default_user"  # Replace with user ID if needed
    if session_id not in conversation_history:
        conversation_history[session_id] = [{"role": "system", "content": system_prompt}]

    conversation_history[session_id].append({"role": "user", "content": message})

    try:
        # Updated OpenAI API call (latest syntax)
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history[session_id]
        )

        ai_response = response.choices[0].message.content
        conversation_history[session_id].append({"role": "assistant", "content": ai_response})

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port, default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)

