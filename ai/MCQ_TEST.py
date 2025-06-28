import google.generativeai as genai

# Configure the API key (you should ideally use an environment variable here)
api_key = "YOUR_GEMINI_API_KEY"  # ⚠️ REPLACE this with os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Model config
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Load Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Start chat session with instructions
chat_session = model.start_chat(history=[
    {
        "role": "user",
        "parts": [
            "Generate a Roadmap in JSON format for the following interest area. "
            "Include chapters, key learning goals, 2–3 YouTube video links, and book links.\n\n"
            "User Interest Area: HTML"
        ],
    },
    {
        "role": "user",
        "parts": [
            "Generate 10 multiple-choice questions (MCQs) for the topic HTML. "
            "Include question, 4 options, correct answer, and 1-line explanation. Return as JSON."
        ],
    }
])

# Ask the final prompt (can be varied for different topics)
response = chat_session.send_message("HTML")

# Output the response
print(response.text)
