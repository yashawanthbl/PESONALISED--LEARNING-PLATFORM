from flask import Blueprint, jsonify, request
import google.generativeai as genai
import nltk
import traceback

# Initialize Blueprint
bot_routes = Blueprint('bot', __name__)

# Configure Gemini API Key
genai.configure(api_key="AIzaSyBL53dBWILLEXRREDVG9x8C2nk1lztEKkI")

# Load Gemini Model
model = genai.GenerativeModel('gemini-pro')

# Start new chat session
chat = model.start_chat(history=[])

# Download nltk data
nltk.download('punkt')


# Function to get Gemini response
def get_gemini_response(question):
    try:
        response = chat.send_message(question)  # Removed stream=True for now
        return response.text
    except Exception as e:
        print("❌ Gemini API Error:", e)
        traceback.print_exc()
        return "Sorry, there was a problem getting a response from Gemini."


# Optional: format the response to HTML
def format_response(response_text):
    formatted_response = ''
    lines = response_text.split('\n')
    for line in lines:
        if '**' in line:
            segments = line.split('**')
            for i, segment in enumerate(segments):
                if i % 2 == 1:
                    segments[i] = f'<b>{segment}</b>'
            line = ''.join(segments)
        formatted_response += f'{line}<br>'
    return formatted_response


# POST route for handling chat input
@bot_routes.route('/ask-chat', methods=['POST'])
def ollama_chat():
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({"error": "Invalid request data"}), 400

        user_input = data.get('prompt')

        if user_input.lower() == 'quit':
            return jsonify({"response": "Exiting the chatbot. Goodbye!"})

        # Get Gemini Response
        response_text = get_gemini_response(user_input)

        # Format for HTML display
        formatted_response = format_response(response_text)

        return jsonify({"response": formatted_response})

    except Exception as e:
        print("❌ Flask Route Error:", e)
        traceback.print_exc()
        return jsonify({"error": "An error occurred while processing your request."}), 500
