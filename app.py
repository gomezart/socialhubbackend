@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    scenario = data.get("scenario")

    if not message or not scenario:
        return jsonify({"error": "Message and scenario are required."}), 400

    # Define scenario-based system prompts
    system_prompts = {
        "dating": "You are a world-class AI dating coach. Engage users in a deep, back-and-forth coaching conversation.",
        "networking": "You are a top networking expert. Guide users with insightful advice and keep the conversation going.",
        "confidence": "You are an expert in confidence-building. Challenge users to reflect and grow through continued discussion."
    }

    system_prompt = system_prompts.get(scenario, "You are an AI assistant providing expert advice.")

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # New AI conversation strategy
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
                {"role": "assistant", "content": "Provide your response with a follow-up question to keep the conversation going."}
            ]
        )

        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
