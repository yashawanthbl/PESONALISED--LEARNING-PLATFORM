import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI SDK with API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Set generation parameters
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Define the function to generate roadmap
def generate_roadmap(user_interest):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Generate a roadmap for the following detail by user interest area. Use this area name to create a full roadmap along with course, video, and book links.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Please provide me with the user's interest area! I need to know what they're interested in before I can create a roadmap.",
                ],
            },
        ]
    )

    response = chat_session.send_message(user_interest)
    return response.text

# CLI usage
if __name__ == "__main__":
    interest = input("Enter your interest area (e.g. Python, AI, Cybersecurity): ")
    output = generate_roadmap(interest)
    print("\n📘 Roadmap Generated:\n")
    print(output)
