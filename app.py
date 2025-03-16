from flask import Flask, request, jsonify, session
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = "your_secret_key"  # Required for session storage

openai.api_key = os.getenv("OPENAI_API_KEY")

# Store conversation history
conversation_history = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    scenario = data.get("scenario")
    
    if not message or not scenario:
        return jsonify({"error": "Message and scenario are required."}), 400
    
    user_id = request.remote_addr  # Temporary user tracking (later use proper auth)
    
    if user_id not in conversation_history:
        conversation_history[user_id] = [
            {"role": "system", "content": f"You are a world-class {scenario} coach. Your goal is to keep the user engaged by always asking follow-up questions."}
        ]
    
    # Add user message to history
    conversation_history[user_id].append({"role": "user", "content": message})

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history[user_id]
        )

        ai_response = response.choices[0].message.content

        # Force a follow-up question
        follow_up_questions = [
            "What are your thoughts on that?",
            "How do you feel about this approach?",
            "Have you ever tried something similar?",
            "What’s your experience with this?",
            "Does this advice make sense to you?",
            "Would you like me to explain more?"
        ]

        if "?" not in ai_response[-5:]:  # If AI didn't naturally ask a question
            ai_response += " " + follow_up_questions[len(conversation_history[user_id]) % len(follow_up_questions)]

        conversation_history[user_id].append({"role": "assistant", "content": ai_response})

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
