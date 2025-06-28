import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Set generation configuration
generation_config = {
    "temperature": 1.35,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

def generate_roadmap(user_interest):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Generate A Roadmap for the following detail by user interest area name. Use this area name to create a full roadmap.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    """{
                        "name": "User Interest Roadmap",
                        "description": "A comprehensive roadmap tailored to the user's specific area of interest.",
                        "timeframe": "Flexible, adaptable to the user's pace and goals.",
                        "status": "Draft, ready for user input and customization.",
                        "milestones": [
                            {"name": "Interest Discovery", "dueDate": "2023-12-15", "description": "Identify and define the user's specific area of interest."},
                            {"name": "Learning Path", "dueDate": "2024-01-31", "description": "Develop a structured learning path."},
                            {"name": "Project-Based Learning", "dueDate": "2024-03-15", "description": "Engage in hands-on projects."},
                            {"name": "Community Building", "dueDate": "2024-04-30", "description": "Connect with like-minded individuals."},
                            {"name": "Continuous Growth", "dueDate": "Ongoing", "description": "Foster continuous learning."}
                        ]
                    }"""
                ],
            },
        ]
    )

    response = chat_session.send_message(user_interest)
    return response.text

if __name__ == "__main__":
    interest = input("Enter your area of interest (e.g., Python, AI, Cybersecurity): ")
    roadmap = generate_roadmap(interest)
    print("\nGenerated Roadmap:\n")
    print(roadmap)
