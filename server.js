require("dotenv").config();
const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(express.json());
app.use(cors());

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_PROJECT_ID = process.env.OPENAI_PROJECT_ID;
const OPENAI_ORG_ID = process.env.OPENAI_ORG_ID;

const PORT = process.env.PORT || 5000;

// Test Route to Check Server is Running
app.get("/", (req, res) => {
    res.send("Server is running ✅");
});

// API Route to Handle AI Responses
app.post("/chat", async (req, res) => {
    try {
        const { message, scenario, gender } = req.body;

        if (!message || !scenario) {
            return res.status(400).json({ error: "Message and scenario are required." });
        }

        const systemPrompt = `You are an expert coach specializing in ${scenario}. Provide highly effective coaching for a ${gender}.`;

        const response = await axios.post(
            "https://api.openai.com/v1/chat/completions",
            {
                model: "gpt-3.5-turbo",
                messages: [
                    { role: "system", content: systemPrompt },
                    { role: "user", content: message }
                ],
                max_tokens: 200
            },
            {
                headers: {
                    "Authorization": `Bearer ${OPENAI_API_KEY}`,
                    "OpenAI-Project": OPENAI_PROJECT_ID,
                    "OpenAI-Organization": OPENAI_ORG_ID,
                    "Content-Type": "application/json"
                }
            }
        );

        res.json({ response: response.data.choices[0].message.content });
    } catch (error) {
        console.error("Error calling OpenAI API:", error.response?.data || error.message);
        res.status(500).json({ error: "Failed to fetch AI response" });
    }
});

// Start Server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT} ✅`);
});
