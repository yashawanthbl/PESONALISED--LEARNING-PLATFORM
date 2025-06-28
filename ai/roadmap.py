import google.generativeai as genai

# Configure your Gemini API key securely (move to .env in production)
api_key = "AIzaSyBJ5ibIkwm1koegM1kCFvq3XtyO-gKFbUI"
genai.configure(api_key=api_key)

# Generation settings
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

# Start chat with initial prompt
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "Generate a roadmap for the following detail by user interest area. Use this area name to create a full roadmap along with course, video, and book links. Output in JSON format.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Please provide me with the user's interest area so I can create a roadmap.\n\nFor example:\n\"User Interest Area: **Machine Learning**\"",
            ],
        },
    ]
)

# Replace this with actual interest area
user_interest_area = "Data Science"

response = chat_session.send_message(f"User Interest Area: {user_interest_area}")

print(response.text)
