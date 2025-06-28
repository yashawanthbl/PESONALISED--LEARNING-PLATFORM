from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

bot_routes = Blueprint('bot', __name__)

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def format_response(response_text):
    lines = response_text.split('\n')
    formatted_response = ''
    for line in lines:
        if '**' in line:
            segments = line.split('**')
            for i, segment in enumerate(segments):
                if i % 2 == 1:
                    segments[i] = f'<b>{segment}</b>'
            line = ''.join(segments)
        formatted_response += f'{line}<br>'
    return formatted_response

@bot_routes.route('/ask-chat', methods=['POST'])
def ollama_chat():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Invalid request data"}), 400

        user_input = data.get('prompt')
        if user_input.lower() == 'quit':
            return jsonify({"response": "Exiting the chatbot. Goodbye!"})

        response = get_gemini_response(user_input)
        response_text = ''.join(chunk.text for chunk in response)
        formatted_response = format_response(response_text)

        return jsonify({"response": formatted_response})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500
